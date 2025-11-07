# Quick Start: 停車場資料查詢站台

## 前置需求

- Python 3.9 或以上版本
- 已安裝的套件（見 requirements.txt）：
  - Flask
  - APScheduler
  - requests
  - beautifulsoup4
  - pandas
  - lxml

## 安裝步驟

### 1. 安裝依賴套件

```bash
pip install Flask APScheduler
```

（其他套件應已從現有專案安裝）

### 2. 確認檔案結構

確保以下檔案存在：
- `app.py` (Flask 主程式)
- `parking_api_taichung.py` (修改後的爬蟲程式)
- `templates/index.html` (前端頁面)

## 啟動程式

### 開發模式

```bash
python app.py
```

程式會：
1. 自動建立 SQLite 資料庫（`data/parking.db`）
2. 啟動 Flask 開發伺服器（預設 http://127.0.0.1:8081）
3. 啟動排程任務（每10分鐘執行一次）

### 首次執行

1. 開啟瀏覽器，前往 http://127.0.0.1:8081
2. 系統會自動執行第一次資料抓取（可能需要1-2分鐘）
3. 之後每10分鐘自動更新

## 使用方式

### 查看停車場資料

1. 開啟網頁 http://127.0.0.1:8081
2. 地圖會自動載入並顯示10個停車場的位置標記
3. 點擊地圖上的停車場標記
4. 會彈出資訊泡泡顯示該停車場的最新資料（名稱、地址、總車位、剩餘車位、更新時間）

### 下載歷史資料

1. 點擊地圖上的停車場標記
2. 在彈出的資訊泡泡中，點擊「下載歷史資料」按鈕
3. 瀏覽器會下載包含該停車場所有歷史記錄的 CSV 檔案

## 停止程式

按 `Ctrl+C` 停止 Flask 伺服器和排程任務。

## 資料庫位置

資料庫檔案位於 `data/parking.db`，包含：
- `parking_lots` 表：停車場基本資訊
- `parking_records` 表：歷史資料記錄

## 排程設定

排程預設為每10分鐘執行一次。如需修改，編輯 `app.py` 中的排程設定：

```python
scheduler.add_job(fetch_and_store_data, 'interval', minutes=10)
```

## 地圖功能

- 地圖使用 Leaflet.js 和 OpenStreetMap 圖資
- 無需 API key，立即可用
- 地圖會自動調整視角以包含所有10個停車場位置
- 點擊標記會顯示資訊泡泡，包含停車場即時資訊和下載按鈕

## 疑難排解

### 無法連線到台中市政府 API

- 檢查網路連線
- 確認 API 網址是否可存取
- 查看終端機的錯誤訊息

### 資料庫錯誤

- 確認 `data/` 目錄存在且有寫入權限
- 刪除 `data/parking.db` 讓系統重新建立

### 排程未執行

- 檢查終端機是否有錯誤訊息
- 確認 APScheduler 已正確啟動
- 手動觸發一次資料抓取測試

