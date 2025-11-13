"""
停車場資料查詢站台 - Flask 主程式
"""

import sqlite3
import os
from flask import Flask, jsonify, render_template, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import io
import csv
from datetime import datetime

# 匯入爬蟲模組
from parking_api_taichung import fetch_parking_data

app = Flask(__name__)

# 資料庫路徑
DB_PATH = 'data/parking.db'

# 目標停車場 ID 列表
TARGET_IDS = [501, 506, 511, 513, 514, 515, 517, 544, 629, 663, 665, 722, 1326, 1529, 1692, 1699, 1715, 1716, 3074]


def init_db():
    """
    初始化資料庫，建立必要的表格和索引
    """
    # 確保 data 目錄存在
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 建立停車場基本資訊表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_lots (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            tot_space INTEGER,
            lon REAL,
            lat REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 建立停車場資料記錄表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parking_lot_id INTEGER NOT NULL,
            update_time TEXT NOT NULL,
            empty_space TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parking_lot_id) REFERENCES parking_lots(id)
        )
    ''')
    
    # 建立索引以加速查詢
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_parking_records_lot_id 
        ON parking_records(parking_lot_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_parking_records_recorded_at 
        ON parking_records(recorded_at DESC)
    ''')
    
    # 建立複合索引以加速去重檢查
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_parking_records_lot_update_time 
        ON parking_records(parking_lot_id, update_time)
    ''')
    
    conn.commit()
    conn.close()
    print('資料庫初始化完成')


def get_db_connection():
    """
    取得資料庫連線
    
    Returns:
        sqlite3.Connection: 資料庫連線物件
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def close_db(conn):
    """
    關閉資料庫連線
    
    Args:
        conn: 資料庫連線物件
    """
    if conn:
        conn.close()


def store_parking_data(df):
    """
    將停車場資料儲存到資料庫（含去重檢查）
    
    Args:
        df (pd.DataFrame): 包含停車場資料的 DataFrame
    """
    if df.empty:
        print('沒有資料可儲存')
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted_count = 0
    skipped_count = 0
    
    try:
        for _, row in df.iterrows():
            parking_id = int(row['id'])
            name = row.get('name', '')
            address = row.get('address', '')
            tot_space = row.get('tot_space', 0)
            lon = row.get('lon', 0.0)
            lat = row.get('lat', 0.0)
            update_time = row.get('update_time', '')
            empty_space = row.get('empty_space', '')
            
            # 插入或更新停車場基本資訊
            cursor.execute('''
                INSERT OR REPLACE INTO parking_lots 
                (id, name, address, tot_space, lon, lat)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (parking_id, name, address, tot_space, lon, lat))
            
            # 檢查是否已存在相同的 parking_lot_id + update_time 組合
            cursor.execute('''
                SELECT EXISTS(
                    SELECT 1 FROM parking_records 
                    WHERE parking_lot_id = ? AND update_time = ?
                )
            ''', (parking_id, update_time))
            
            exists = cursor.fetchone()[0]
            
            if not exists:
                # 如果不存在，插入新的記錄
                cursor.execute('''
                    INSERT INTO parking_records 
                    (parking_lot_id, update_time, empty_space)
                    VALUES (?, ?, ?)
                ''', (parking_id, update_time, empty_space))
                inserted_count += 1
            else:
                # 如果已存在，跳過該筆記錄
                skipped_count += 1
        
        conn.commit()
        print(f'成功儲存 {inserted_count} 筆新資料，跳過 {skipped_count} 筆重複資料（共處理 {len(df)} 筆）')
    except Exception as e:
        conn.rollback()
        print(f'儲存資料時發生錯誤: {e}')
    finally:
        close_db(conn)


# 初始化資料庫
init_db()


# Flask Routes

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/parking/list')
def get_parking_list():
    """取得所有停車場的基本資訊列表（用於下拉選單）"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, address, tot_space, lon, lat
            FROM parking_lots
            ORDER BY id
        ''')
        
        parking_lots = []
        for row in cursor.fetchall():
            parking_lots.append({
                'id': row['id'],
                'name': row['name'],
                'address': row['address'],
                'tot_space': row['tot_space'],
                'lon': row['lon'],
                'lat': row['lat']
            })
        
        close_db(conn)
        return jsonify({'parking_lots': parking_lots})
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


@app.route('/api/parking/<int:parking_id>/latest')
def get_parking_latest(parking_id):
    """取得指定停車場的最新資料"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 取得停車場基本資訊
        cursor.execute('''
            SELECT id, name, address, tot_space, lon, lat
            FROM parking_lots
            WHERE id = ?
        ''', (parking_id,))
        
        lot = cursor.fetchone()
        if not lot:
            close_db(conn)
            return jsonify({'error': '停車場不存在', 'code': 404}), 404
        
        # 取得最新一筆記錄
        cursor.execute('''
            SELECT update_time, empty_space, recorded_at
            FROM parking_records
            WHERE parking_lot_id = ?
            ORDER BY recorded_at DESC
            LIMIT 1
        ''', (parking_id,))
        
        record = cursor.fetchone()
        
        close_db(conn)
        
        result = {
            'id': lot['id'],
            'name': lot['name'],
            'address': lot['address'],
            'tot_space': lot['tot_space'],
            'lon': lot['lon'],
            'lat': lot['lat']
        }
        
        if record:
            result['update_time'] = record['update_time']
            result['empty_space'] = record['empty_space']
            result['recorded_at'] = record['recorded_at']
        else:
            result['update_time'] = None
            result['empty_space'] = None
            result['recorded_at'] = None
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


@app.route('/api/parking/<int:parking_id>/download')
def download_parking_data(parking_id):
    """下載指定停車場的所有歷史資料（CSV格式）"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 取得停車場基本資訊
        cursor.execute('''
            SELECT id, name, address, tot_space, lon, lat
            FROM parking_lots
            WHERE id = ?
        ''', (parking_id,))
        
        lot = cursor.fetchone()
        if not lot:
            close_db(conn)
            return jsonify({'error': '停車場不存在', 'code': 404}), 404
        
        # 取得所有歷史記錄
        cursor.execute('''
            SELECT update_time, empty_space, recorded_at
            FROM parking_records
            WHERE parking_lot_id = ?
            ORDER BY recorded_at ASC
        ''', (parking_id,))
        
        records = cursor.fetchall()
        close_db(conn)
        
        # 建立 CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 寫入標題列
        writer.writerow(['id', 'name', 'address', 'tot_space', 'empty_space', 'update_time', 'lon', 'lat', 'recorded_at'])
        
        # 寫入資料列
        for record in records:
            writer.writerow([
                lot['id'],
                lot['name'],
                lot['address'],
                lot['tot_space'],
                record['empty_space'],
                record['update_time'],
                lot['lon'],
                lot['lat'],
                record['recorded_at']
            ])
        
        # 建立回應
        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'parking_{parking_id}_{timestamp}.csv'
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


def fetch_and_store_data():
    """排程任務：取得停車場資料並儲存到資料庫"""
    print(f'[{datetime.now()}] 開始執行排程任務：取得停車場資料')
    try:
        # 使用預設的目標 ID 列表
        df = fetch_parking_data(TARGET_IDS)
        if not df.empty:
            store_parking_data(df)
            print(f'[{datetime.now()}] 排程任務完成：成功儲存 {len(df)} 筆資料')
        else:
            print(f'[{datetime.now()}] 排程任務完成：未取得任何資料')
    except Exception as e:
        print(f'[{datetime.now()}] 排程任務失敗：{e}')


# 設定排程器
scheduler = BackgroundScheduler()
scheduler.add_job(
    fetch_and_store_data,
    'interval',
    minutes=10,
    id='fetch_parking_data',
    name='取得停車場資料',
    replace_existing=True
)
scheduler.start()
print('排程器已啟動：每10分鐘執行一次資料抓取')

# 啟動時立即執行一次資料抓取
fetch_and_store_data()


if __name__ == '__main__':
    # 啟動時執行一次資料抓取
    fetch_and_store_data()
    # 生產環境使用環境變數 PORT，開發環境使用 8081
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=False, host='0.0.0.0', port=port)

