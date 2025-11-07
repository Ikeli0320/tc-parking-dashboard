# Research: 停車場資料查詢站台

## Technology Choices

### Web Framework: Flask

**Decision**: 使用 Flask 作為後端框架

**Rationale**: 
- 最簡單的 Python Web 框架，學習曲線低
- 無需複雜設定即可啟動
- 符合專案憲法的「快速交付」原則
- 足夠處理簡單的 API 和網頁需求

**Alternatives considered**:
- FastAPI: 功能更強大但設定較複雜，不符合最小範圍原則
- Django: 過於龐大，包含許多不需要的功能
- 純 Python HTTP server: 功能不足，需要自行實作路由

### Database: SQLite

**Decision**: 使用 SQLite 儲存累積的歷史資料

**Rationale**:
- Python 內建支援，無需額外安裝
- 單一檔案，易於備份和部署
- 足夠處理小規模資料（10個停車場，每30分鐘一筆）
- 符合「立即可執行」原則

**Alternatives considered**:
- PostgreSQL/MySQL: 需要額外安裝和設定，不符合最小範圍
- CSV 檔案: 查詢效率低，不符合需求
- JSON 檔案: 不適合累積大量資料

### Scheduling: APScheduler

**Decision**: 使用 APScheduler 執行每10分鐘的排程任務

**Rationale**:
- 簡單易用，可在 Flask 應用程式中整合
- 支援背景執行，不阻塞主程式
- 符合「立即可執行」原則
- 10分鐘的頻率可提供更即時的資料更新

**Alternatives considered**:
- schedule 套件: 功能較簡單，但可能不夠穩定
- cron (系統層級): 需要額外設定，不符合立即可執行原則
- Celery: 過於複雜，不符合最小範圍

### Frontend: 純 HTML + JavaScript + Leaflet.js

**Decision**: 使用單一 HTML 檔案，內嵌 JavaScript，使用 Leaflet.js 地圖庫（CDN載入）

**Rationale**:
- 最簡單的方式，無需建置工具
- 符合「快速交付」和「立即可執行」原則
- Leaflet.js 是開源地圖庫，無需 API key，立即可用
- 透過 CDN 載入，無需額外安裝
- 足夠處理地圖顯示、標記、資訊泡泡等功能

**Alternatives considered**:
- Google Maps API: 需要 API key 和付費，不符合立即可執行原則
- OpenStreetMap + Leaflet: 開源且免費，符合需求（Leaflet 使用 OpenStreetMap 圖資）
- Mapbox: 需要 API key，不符合立即可執行原則
- React/Vue: 需要建置工具和複雜設定，不符合最小範圍
- jQuery: 雖然簡單，但非必要，純 JavaScript 已足夠

### Map Library: Leaflet.js

**Decision**: 使用 Leaflet.js 作為地圖庫

**Rationale**:
- 開源免費，無需 API key
- 輕量級（約 40KB），載入快速
- 透過 CDN 載入，無需額外安裝
- 支援標記（Marker）和資訊視窗（Popup）
- 符合「立即可執行」原則
- 使用 OpenStreetMap 圖資，無需額外設定

**Alternatives considered**:
- Google Maps JavaScript API: 需要 API key，不符合立即可執行原則
- Mapbox GL JS: 需要 API key，不符合立即可執行原則
- OpenLayers: 功能過於複雜，不符合最小範圍原則

## Integration Patterns

### 整合現有爬蟲程式

**Decision**: 將 `parking_api_taichung.py` 的 `main()` 函數修改為可被匯入的模組，並將核心邏輯提取為可重複使用的函數

**Rationale**:
- 不重寫現有程式碼，符合「快速交付」原則
- 透過函數匯入的方式，避免程式碼重複
- 保持現有程式的獨立性（仍可單獨執行）

**Implementation approach**:
- 將 `main()` 函數改為 `fetch_parking_data(target_ids=None)`
- 返回處理後的 DataFrame，而非直接儲存 CSV
- 保留原有的錯誤處理邏輯

### 資料儲存策略

**Decision**: 每次排程執行後，在存入資料前檢查是否已存在相同的 `update_time`，如果不存在才插入新資料

**Rationale**:
- 符合「資料累積」需求
- 避免重複資料（當資料來源的 `update_time` 未變更時）
- SQLite 的 INSERT 操作簡單快速
- 使用 SQL EXISTS 查詢進行去重檢查，簡單高效
- 可透過 SQL 查詢輕鬆取得歷史資料

**Database schema**:
- `parking_lots` 表：儲存停車場基本資訊（id, name, address, tot_space, lon, lat）
- `parking_records` 表：儲存歷史記錄（id, parking_lot_id, update_time, empty_space）

**去重邏輯**:
- 在插入 `parking_records` 前，使用 SQL EXISTS 查詢檢查是否已存在相同的 `parking_lot_id` + `update_time` 組合
- 如果已存在，跳過該筆記錄
- 如果不存在，插入新記錄
- 此機制確保相同 `update_time` 的資料不會重複儲存

## Performance Considerations

### 資料量估算

- 10個停車場 × 每10分鐘一筆（如果資料有更新）= 每天最多 1,440 筆記錄
- 實際記錄數取決於資料來源的更新頻率（如果 `update_time` 未變更，不會新增記錄）
- 一個月約 43,200 筆記錄（如果每天都有更新）
- SQLite 可輕鬆處理此規模的資料

### 查詢優化

- 使用索引加速查詢（parking_lot_id, update_time）
- 前端僅顯示最新一筆資料，減少資料傳輸
- 下載功能使用簡單的 SQL SELECT，無需複雜查詢

## Deployment Considerations

### 執行方式

**Decision**: 單一 Python 程式（app.py）啟動所有功能

**Rationale**:
- Flask 內建開發伺服器，可直接執行
- APScheduler 在背景執行排程
- 符合「立即可執行」原則

**啟動指令**:
```bash
python app.py
```

### 生產環境考量

**Note**: 根據專案憲法，不進行長期維運設計。如需部署到生產環境，可後續考慮使用 gunicorn 或 uWSGI，但不在本次範圍內。

