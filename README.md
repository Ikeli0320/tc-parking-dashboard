# 台中市停車場資料爬蟲程式

這是一個用於爬取台中市停車場即時資訊的 Python 程式，可以取得停車場的位置、名稱、地址、總車位數、剩餘車位數等資料。

## 功能特色

- 📍 從台中市政府 API 取得停車場位置資訊（經緯度）
- 🚗 爬取各停車場的即時剩餘車位資訊
- 📊 整合並合併停車場位置與詳細資訊
- 💾 自動儲存為 CSV 檔案（UTF-8 編碼）
- 🧪 支援測試模式，可快速測試程式功能

## 系統需求

- Python 3.6 或以上版本
- 所需的 Python 套件（見下方安裝說明）

## 安裝步驟

### 1. 建立虛擬環境（建議）

建議使用虛擬環境來管理專案依賴，避免與系統 Python 環境衝突：

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

啟動虛擬環境後，終端機提示字元前會顯示 `(venv)`。

### 2. 安裝 Python 套件

在虛擬環境中安裝所需的套件：

```bash
# 使用 requirements.txt 安裝所有依賴套件（推薦）
pip install -r requirements.txt
```

或手動安裝套件：

```bash
pip install requests beautifulsoup4 pandas lxml
```

### 3. 確認程式檔案

確保 `parking_api_taichung.py` 檔案在當前目錄中。

### 4. 退出虛擬環境（選用）

使用完畢後，可以退出虛擬環境：

```bash
deactivate
```

## 使用方法

### 基本執行

**注意：請確保已啟動虛擬環境（如果使用虛擬環境）**

直接執行程式，會爬取所有停車場的資料：

```bash
# 如果使用虛擬環境，請先啟動
source venv/bin/activate  # macOS/Linux

# 執行程式
python parking_api_taichung.py
```

### 測試模式

如果要先測試程式功能，可以修改程式碼中的 `main()` 函數呼叫：

```python
# 測試模式：只爬取前 10 筆資料
main(test_mode=True, test_limit=10)
```

### 輸出檔案

程式執行完成後，會在 `output` 目錄下產生 CSV 檔案，檔名格式為：
```
parking_empty_space_YYYY-MM-DD_HH-MM-SS.csv
```

## 輸出資料格式

CSV 檔案包含以下欄位：

| 欄位名稱 | 說明 |
|---------|------|
| id | 停車場 ID |
| update_time | 資料更新時間 |
| name | 停車場名稱 |
| address | 停車場地址 |
| tot_space | 總車位數 |
| empty_space | 剩餘車位數 |
| lon | 經度 |
| lat | 緯度 |

## 程式架構

程式主要包含以下函數：

- `get_parking_locations()`: 從 API 取得停車場位置資訊
- `get_showparking_table(input_id)`: 取得指定停車場的詳細資訊
- `get_parking_space_info()`: 批次取得所有停車場的剩餘車位資訊
- `merge_parking_data()`: 合併停車場詳細資訊與位置資訊
- `save_to_csv()`: 將資料儲存為 CSV 檔案
- `main()`: 主程式流程

## 注意事項

1. **網路連線**: 程式需要穩定的網路連線來存取台中市政府的 API 和網頁
2. **執行時間**: 完整爬取所有停車場資料可能需要一些時間，請耐心等待
3. **資料格式**: 程式會自動過濾不符合標準格式的資料，只保留有「剩餘車位數」欄位的停車場
4. **錯誤處理**: 程式包含基本的錯誤處理機制，會跳過無法取得的停車場資料

## 資料來源

- 停車場位置 API: `https://motoretag.taichung.gov.tw/DataAPI/api/ParkingAPIV2`
- 停車場詳細資訊: `https://e-traffic.taichung.gov.tw/ATIS_TCC/Device/Showparking`

## 授權

本程式僅供學習和研究使用。使用時請遵守台中市政府網站的服務條款和使用規範。

## 問題回報

如有任何問題或建議，歡迎提出 Issue。

