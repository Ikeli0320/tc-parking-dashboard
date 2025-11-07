# API Contracts: 停車場資料查詢站台

## Base URL

所有 API 端點的前綴為 `/api`

## Endpoints

### GET /api/parking/list

取得所有停車場的基本資訊列表（用於地圖標記）。

**Request**:
- Method: GET
- Parameters: 無

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "parking_lots": [
    {
      "id": 501,
      "name": "大雅區-交通局-大雅永興P",
      "address": "台中市大雅區大雅路151號旁",
      "tot_space": 30,
      "lon": 120.647652,
      "lat": 24.2253971
    },
    ...
  ]
}
```

**Error Responses**:
- 500: 伺服器錯誤

---

### GET /api/parking/<id>/latest

取得指定停車場的最新資料。

**Request**:
- Method: GET
- Path Parameters:
  - `id` (integer): 停車場 ID（501, 506, 517, 544, 629, 663, 665, 1326, 1692, 1699）

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": 501,
  "name": "大雅區-交通局-大雅永興P",
  "address": "台中市大雅區大雅路151號旁",
  "tot_space": 30,
  "empty_space": "無資訊",
  "update_time": "2025/11/07 11:32 更新",
  "lon": 120.647652,
  "lat": 24.2253971,
  "recorded_at": "2025-01-27 11:32:00"
}
```

**Error Responses**:
- 404: 停車場不存在
- 500: 伺服器錯誤

---

### GET /api/parking/<id>/download

下載指定停車場的所有歷史資料（CSV格式）。

**Request**:
- Method: GET
- Path Parameters:
  - `id` (integer): 停車場 ID

**Response**:
- Status: 200 OK
- Content-Type: text/csv
- Headers:
  - `Content-Disposition: attachment; filename="parking_<id>_<timestamp>.csv"`
- Body: CSV 格式的資料
```csv
id,name,address,tot_space,empty_space,update_time,lon,lat,recorded_at
501,大雅區-交通局-大雅永興P,台中市大雅區大雅路151號旁,30,無資訊,2025/11/07 11:32 更新,120.647652,24.2253971,2025-01-27 11:32:00
501,大雅區-交通局-大雅永興P,台中市大雅區大雅路151號旁,30,15,2025/11/07 12:02 更新,120.647652,24.2253971,2025-01-27 12:02:00
...
```

**Error Responses**:
- 404: 停車場不存在
- 500: 伺服器錯誤

---

### GET /

主頁面（HTML）。

**Request**:
- Method: GET

**Response**:
- Status: 200 OK
- Content-Type: text/html
- Body: HTML 頁面（包含地圖介面、標記、資訊泡泡、下載按鈕）

---

## Data Types

### ParkingLot Object

```json
{
  "id": 501,
  "name": "大雅區-交通局-大雅永興P",
  "address": "台中市大雅區大雅路151號旁",
  "tot_space": 30,
  "lon": 120.647652,
  "lat": 24.2253971
}
```

### ParkingRecord Object

```json
{
  "id": 501,
  "name": "大雅區-交通局-大雅永興P",
  "address": "台中市大雅區大雅路151號旁",
  "tot_space": 30,
  "empty_space": "無資訊",
  "update_time": "2025/11/07 11:32 更新",
  "lon": 120.647652,
  "lat": 24.2253971,
  "recorded_at": "2025-01-27 11:32:00"
}
```

## Error Response Format

所有錯誤回應使用統一格式：

```json
{
  "error": "錯誤訊息",
  "code": 404
}
```

