"""
台中市停車場資料爬蟲程式
從台中市政府 API 取得停車場資訊並整合剩餘車位資料
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import os


def get_parking_locations():
    """
    從台中市政府 API 取得停車場位置資訊
    
    Returns:
        pd.DataFrame: 包含停車場 ID、位置、經緯度的 DataFrame
    """
    parking_light_url = "https://motoretag.taichung.gov.tw/DataAPI/api/ParkingAPIV2"
    
    try:
        response = requests.get(parking_light_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        parking_light_df = pd.DataFrame(data)
        parking_light_df = parking_light_df[["ID", "Position", "X", "Y"]]
        parking_light_df.columns = ['id', 'position', 'lon', 'lat']
        print(f'成功取得停車場位置資料: {parking_light_df.shape[0]} 筆')
        return parking_light_df
    except requests.exceptions.RequestException as e:
        print(f'取得停車場位置資料時發生錯誤: {e}')
        return pd.DataFrame()


def get_showparking_table(input_id):
    """
    取得指定停車場的詳細資訊
    
    Args:
        input_id (str): 停車場 ID
    
    Returns:
        list: 包含停車場 ID、更新時間與所有欄位資訊的列表
    """
    url = f"https://e-traffic.taichung.gov.tw/ATIS_TCC/Device/Showparking?id={input_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 取得右側對齊的 div，通常包含更新時間
        update_div = soup.find("div", align="right")
        update_text = update_div.get_text(strip=True) if update_div else None
        
        # 使用正則表達式擷取所有 <td> 標籤的內容
        td_strings = re.findall(r'<td[^>]*?>.*?</td>', response.text, flags=re.DOTALL)
        td_strings = [re.sub(r'</?td[^>]*?>', '', s).strip() 
                     for s in td_strings 
                     if re.sub(r'</?td[^>]*?>', '', s).strip()]
        
        # 將停車場 id、更新時間與所有欄位資訊組成一個 list
        parking_space_info = [input_id] + [update_text] + td_strings
        
        return parking_space_info
    except requests.exceptions.RequestException as e:
        print(f'取得停車場 {input_id} 資訊時發生錯誤: {e}')
        return None


def get_parking_space_info(parking_light_df, target_ids=None):
    """
    取得指定停車場的剩餘車位資訊
    
    Args:
        parking_light_df (pd.DataFrame): 停車場位置資料
        target_ids (list): 要抓取的停車場 ID 列表，如果為 None 則抓取所有
    
    Returns:
        pd.DataFrame: 包含停車場詳細資訊的 DataFrame
    """
    parking_space_list = []
    
    # 如果指定了目標 ID，則只處理這些 ID
    if target_ids is not None:
        # 確保 ID 為字串格式以便比對
        target_ids = [str(id) for id in target_ids]
        # 過濾出只包含目標 ID 的資料
        parking_light_df = parking_light_df[parking_light_df['id'].astype(str).isin(target_ids)]
        total_count = len(parking_light_df)
        print(f'開始爬取指定停車場資訊: 共 {total_count} 筆')
    else:
        total_count = len(parking_light_df)
        print(f'開始爬取所有停車場資訊: 共 {total_count} 筆')
    
    for i in range(total_count):
        parking_id = parking_light_df['id'].iloc[i]
        print(f'[{i+1}/{total_count}] 處理停車場 ID: {parking_id}')
        
        parking_space = get_showparking_table(parking_id)
        if parking_space:
            parking_space_list.append(parking_space)
    
    if not parking_space_list:
        print('未取得任何停車場資訊')
        return pd.DataFrame()
    
    # 將資料轉為 DataFrame
    parking_space_df = pd.DataFrame(parking_space_list)
    
    # 剩餘車格數資料清理，保留大部分通用格式，沒有這個欄位或是欄位對不上的直接被排除
    if len(parking_space_df.columns) > 7:
        parking_space_df = parking_space_df[parking_space_df.iloc[:, 7] == '剩餘車位數']
        parking_space_df = parking_space_df.iloc[:, 0:9]
        parking_space_df = parking_space_df.iloc[:, [0, 1, 2, 4, 6, 8]]
        parking_space_df.columns = ['id', 'update_time', 'name', 'address', 'tot_space', 'empty_space']
    
    print(f'成功取得停車場詳細資訊: {parking_space_df.shape[0]} 筆')
    return parking_space_df


def merge_parking_data(parking_space_df, parking_light_df):
    """
    合併停車場詳細資訊與位置資訊
    
    Args:
        parking_space_df (pd.DataFrame): 停車場詳細資訊
        parking_light_df (pd.DataFrame): 停車場位置資訊
    
    Returns:
        pd.DataFrame: 合併後的完整停車場資料
    """
    parking_empty_space_df = pd.merge(
        parking_space_df, 
        parking_light_df, 
        left_on="id", 
        right_on="id", 
        how="inner"
    )
    parking_empty_space_df = parking_empty_space_df.drop(columns=['position'])
    print(f'合併後資料筆數: {parking_empty_space_df.shape[0]} 筆')
    return parking_empty_space_df


def save_to_csv(dataframe, output_dir='output'):
    """
    將資料儲存為 CSV 檔案
    
    Args:
        dataframe (pd.DataFrame): 要儲存的資料
        output_dir (str): 輸出目錄
    
    Returns:
        str: 儲存的檔案名稱
    """
    # 建立輸出目錄（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    runtime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(output_dir, f'parking_empty_space_{runtime}.csv')
    
    dataframe.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'資料已儲存至: {filename}')
    return filename


def fetch_parking_data(target_ids=None):
    """
    取得停車場資料並返回 DataFrame（不儲存 CSV）
    
    Args:
        target_ids (list): 要抓取的停車場 ID 列表，如果為 None 則使用預設的 19 個 ID
    
    Returns:
        pd.DataFrame: 包含停車場完整資料的 DataFrame，如果失敗則返回空的 DataFrame
    """
    # 定義目標停車場 ID 列表
    if target_ids is None:
        # 預設只抓取指定的停車場 ID
        target_ids = [501, 506, 511, 513, 514, 515, 517, 544, 629, 663, 665, 722, 1326, 1529, 1692, 1699, 1715, 1716, 3074]
    
    # 取得停車場位置資料
    parking_light_df = get_parking_locations()
    if parking_light_df.empty:
        print('無法取得停車場位置資料')
        return pd.DataFrame()
    
    # 取得停車場詳細資訊（只處理目標 ID）
    parking_space_df = get_parking_space_info(parking_light_df, target_ids)
    if parking_space_df.empty:
        print('無法取得停車場詳細資訊')
        return pd.DataFrame()
    
    # 合併資料
    parking_empty_space_df = merge_parking_data(parking_space_df, parking_light_df)
    
    return parking_empty_space_df


def main(target_ids=None):
    """
    主程式（保留原有功能，用於獨立執行）
    
    Args:
        target_ids (list): 要抓取的停車場 ID 列表，如果為 None 則抓取所有
    """
    print('=' * 50)
    print('台中市停車場資料爬蟲程式')
    print('=' * 50)
    
    # 定義目標停車場 ID 列表
    if target_ids is None:
        # 預設只抓取指定的停車場 ID
        target_ids = [501, 506, 511, 513, 514, 515, 517, 544, 629, 663, 665, 722, 1326, 1529, 1692, 1699, 1715, 1716, 3074]
        print(f'使用預設目標 ID: {target_ids}')
    else:
        print(f'使用指定目標 ID: {target_ids}')
    
    # 使用 fetch_parking_data 取得資料
    parking_empty_space_df = fetch_parking_data(target_ids)
    
    # 儲存資料
    if not parking_empty_space_df.empty:
        save_to_csv(parking_empty_space_df)
        print('=' * 50)
        print('程式執行完成')
        print('=' * 50)
    else:
        print('沒有資料可儲存')


if __name__ == "__main__":
    # 執行主程式，只抓取指定的停車場 ID
    main()
