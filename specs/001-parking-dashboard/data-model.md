# Data Model: 停車場資料查詢站台

## Entities

### ParkingLot (停車場基本資訊)

**Purpose**: 儲存停車場的靜態資訊，這些資訊不會頻繁變動。

**Fields**:
- `id` (INTEGER, PRIMARY KEY): 停車場 ID（501, 506, 517, 544, 629, 663, 665, 1326, 1692, 1699）
- `name` (TEXT): 停車場名稱（如「大雅區-交通局-大雅永興P」）
- `address` (TEXT): 停車場地址
- `tot_space` (INTEGER): 總車位數
- `lon` (REAL): 經度
- `lat` (REAL): 緯度
- `created_at` (TIMESTAMP): 建立時間

**Validation Rules**:
- `id` 必須是 10 個指定 ID 之一
- `tot_space` 必須 > 0
- `lon`, `lat` 必須是有效的經緯度範圍

**Relationships**:
- 一對多：一個 ParkingLot 可以有多筆 ParkingRecord

### ParkingRecord (停車場資料記錄)

**Purpose**: 儲存每次排程執行時取得的即時剩餘車位資料，資料會累積不覆蓋。

**Fields**:
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT): 記錄 ID
- `parking_lot_id` (INTEGER, FOREIGN KEY): 關聯到 ParkingLot.id
- `update_time` (TEXT): 資料更新時間（從爬蟲取得，格式如「2025/11/07 11:32 更新」）
- `empty_space` (TEXT): 剩餘車位數（可能是數字或「無資訊」）
- `recorded_at` (TIMESTAMP): 記錄建立時間（系統時間）

**Validation Rules**:
- `parking_lot_id` 必須存在於 ParkingLot 表中
- `update_time` 不能為空
- `recorded_at` 自動設定為當前時間

**Relationships**:
- 多對一：多筆 ParkingRecord 關聯到一個 ParkingLot

## Database Schema

### SQLite Table Definitions

```sql
-- 停車場基本資訊表
CREATE TABLE IF NOT EXISTS parking_lots (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    tot_space INTEGER,
    lon REAL,
    lat REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 停車場資料記錄表
CREATE TABLE IF NOT EXISTS parking_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_lot_id INTEGER NOT NULL,
    update_time TEXT NOT NULL,
    empty_space TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parking_lot_id) REFERENCES parking_lots(id)
);

-- 建立索引以加速查詢
CREATE INDEX IF NOT EXISTS idx_parking_records_lot_id ON parking_records(parking_lot_id);
CREATE INDEX IF NOT EXISTS idx_parking_records_recorded_at ON parking_records(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_parking_records_lot_update_time ON parking_records(parking_lot_id, update_time);
```

## Data Flow

### 排程執行流程

1. APScheduler 每10分鐘觸發排程任務
2. 呼叫修改後的 `parking_api_taichung.py` 中的函數，取得10個停車場的資料
3. 對於每個停車場：
   - 檢查 `parking_lots` 表中是否存在該 ID
   - 如果不存在，插入新的 ParkingLot 記錄
   - 如果已存在但資訊有變更，更新 ParkingLot 記錄
   - **資料去重檢查**：檢查 `parking_records` 表中是否已存在相同的 `parking_lot_id` + `update_time` 組合
   - 如果不存在相同的 `update_time`，才插入新的 ParkingRecord 記錄（避免重複資料）
   - 如果已存在相同的 `update_time`，跳過該筆記錄（資料未更新）

### 查詢流程

1. 使用者選擇停車場（透過下拉選單）
2. 前端發送 AJAX 請求到 `/api/parking/<id>/latest`
3. 後端查詢：
   - 從 `parking_lots` 取得停車場基本資訊
   - 從 `parking_records` 取得最新一筆記錄（ORDER BY recorded_at DESC LIMIT 1）
4. 返回 JSON 資料給前端顯示

### 下載流程

1. 使用者點擊下載按鈕
2. 前端發送請求到 `/api/parking/<id>/download`
3. 後端查詢：
   - 從 `parking_lots` 取得停車場基本資訊
   - 從 `parking_records` 取得所有歷史記錄（ORDER BY recorded_at ASC）
4. 將資料轉換為 CSV 格式並返回

## State Management

### ParkingLot 狀態

- **初始狀態**: 第一次排程執行時建立
- **更新狀態**: 如果爬蟲取得的資訊有變更（如地址、總車位數），更新記錄
- **狀態不變**: 如果資訊相同，僅新增 ParkingRecord

### ParkingRecord 狀態

- **新增**: 每次排程執行時，如果 `update_time` 與資料庫中現有記錄不同，才新增記錄
- **跳過**: 如果 `update_time` 已存在於資料庫中，跳過該筆記錄（避免重複）
- **累積**: 所有歷史記錄都保留，用於下載功能
- **去重機制**: 基於 `parking_lot_id` + `update_time` 的唯一性檢查

