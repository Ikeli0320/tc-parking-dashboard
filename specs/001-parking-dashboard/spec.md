# Feature Specification: 停車場資料查詢站台

**Feature Branch**: `001-parking-dashboard`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: 參考 parking_api_taichung.py，建立開放性站台供企劃查看和下載停車場資料

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 查看停車場即時資料 (Priority: P1)

企劃人員可以透過網頁瀏覽器開啟站台，在地圖上看到10個停車場的位置標記，點擊標記後彈出泡泡顯示該停車場的即時剩餘車格狀態。

**Why this priority**: 這是核心功能，必須先完成才能提供基本價值。

**Independent Test**: 開啟網頁，應顯示地圖和10個停車場標記，點擊任一標記，應彈出泡泡顯示該停車場的最新資料（包含名稱、地址、總車位、剩餘車位、更新時間）。

**Acceptance Scenarios**:

1. **Given** 站台已啟動，**When** 企劃開啟網頁，**Then** 應顯示地圖介面，地圖上標示10個停車場位置
2. **Given** 地圖顯示10個停車場標記，**When** 企劃點擊任一標記，**Then** 應彈出資訊泡泡顯示該停車場的即時資料（名稱、地址、總車位、剩餘車位、更新時間）
3. **Given** 資料已更新，**When** 企劃點擊停車場標記，**Then** 應顯示最新的剩餘車位數和更新時間
4. **Given** 資訊泡泡已顯示，**When** 企劃點擊下載按鈕，**Then** 應下載該停車場的歷史資料CSV檔案

---

### User Story 2 - 下載歷史資料 (Priority: P2)

企劃人員可以下載指定停車場的歷史累積資料（CSV格式）。

**Why this priority**: 下載功能是核心需求之一，但可以獨立於查看功能實作。

**Independent Test**: 選擇停車場後，點擊下載按鈕，應能下載包含該停車場所有歷史記錄的CSV檔案。

**Acceptance Scenarios**:

1. **Given** 已選擇停車場，**When** 企劃點擊下載按鈕，**Then** 應下載包含該停車場所有歷史資料的CSV檔案
2. **Given** 資料庫中有累積的歷史資料，**When** 下載CSV，**Then** CSV應包含所有時間點的記錄（時間、剩餘車位等）

---

### Edge Cases

- 如果某個停車場的資料尚未更新（排程尚未執行），應顯示「資料更新中」或最後一次更新的時間
- 如果資料庫中沒有某個停車場的資料，應顯示適當的提示訊息
- 如果網路連線中斷導致無法取得最新資料，應顯示錯誤訊息但保留最後一次成功的資料

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系統 MUST 提供網頁介面，無需帳密即可存取
- **FR-002**: 系統 MUST 提供地圖介面，在地圖上標示10個指定停車場的位置（ID: 501, 506, 517, 544, 629, 663, 665, 1326, 1692, 1699）
- **FR-003**: 系統 MUST 每10分鐘自動呼叫現有的爬蟲程式，取得10個停車場的即時剩餘車格狀態
- **FR-004**: 系統 MUST 將每次取得的資料累積儲存（不覆蓋舊資料），但在存入資料前必須檢查是否已存在相同的更新時間(update_time)，如果不存在才新增資料
- **FR-005**: 系統 MUST 在點擊地圖標記時彈出資訊泡泡，顯示該停車場的最新資料（名稱、地址、總車位、剩餘車位、更新時間）
- **FR-008**: 系統 MUST 在地圖資訊泡泡中提供下載歷史資料的按鈕
- **FR-006**: 系統 MUST 提供下載功能，可下載指定停車場的所有歷史資料（CSV格式）
- **FR-007**: 系統 MUST 使用現有的 `parking_api_taichung.py` 程式邏輯來取得資料

### Key Entities *(include if feature involves data)*

- **ParkingLot**: 停車場基本資訊（id, name, address, tot_space, lon, lat）
- **ParkingRecord**: 停車場資料記錄（id, update_time, empty_space, 關聯到 ParkingLot）

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 企劃可以在5秒內開啟網頁並查看任一停車場的資料
- **SC-002**: 系統每10分鐘自動更新資料，誤差在±1分鐘內
- **SC-003**: 下載的CSV檔案包含完整的歷史資料，格式正確可用Excel開啟
- **SC-004**: 網頁介面在主流瀏覽器（Chrome, Firefox, Safari）中正常運作

