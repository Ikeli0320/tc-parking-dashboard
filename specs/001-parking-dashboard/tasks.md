# Tasks: 停車場資料查詢站台（地圖介面版）

**Input**: Design documents from `/specs/001-parking-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: 根據專案憲法，不建立自動化測試套件，僅進行手動測試。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: 單一專案結構，檔案位於 repository root
- `app.py`: Flask 主程式
- `parking_api_taichung.py`: 修改後的爬蟲模組
- `templates/index.html`: 前端頁面（地圖介面）
- `data/parking.db`: SQLite 資料庫

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (data/, templates/, static/ directories)
- [X] T002 Update requirements.txt to include Flask and APScheduler dependencies
- [X] T003 [P] Create data/ directory for SQLite database storage

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Modify parking_api_taichung.py to extract fetch_parking_data() function that returns DataFrame instead of saving CSV
- [X] T005 Modify parking_api_taichung.py to make main() function callable with target_ids parameter
- [X] T006 Create database initialization function in app.py to create SQLite schema (parking_lots and parking_records tables with indexes)
- [X] T007 Create database helper functions in app.py (init_db(), get_db_connection(), close_db())
- [X] T008 Create data storage function in app.py (store_parking_data()) to insert/update parking_lots and insert parking_records
- [X] T034 Update database initialization in app.py to add composite index idx_parking_records_lot_update_time on (parking_lot_id, update_time) for deduplication performance
- [X] T035 Modify store_parking_data() function in app.py to check for existing records with same parking_lot_id + update_time before inserting
- [X] T036 Add SQL EXISTS query in store_parking_data() to check if parking_records already contains the same update_time for each parking_lot_id
- [X] T037 Update store_parking_data() to skip inserting ParkingRecord if duplicate update_time is found, and log the skip action

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 查看停車場即時資料（地圖介面） (Priority: P1) 🎯 MVP

**Goal**: 企劃人員可以透過網頁瀏覽器開啟站台，在地圖上看到10個停車場的位置標記，點擊標記後彈出泡泡顯示該停車場的即時剩餘車格狀態。

**Independent Test**: 開啟網頁 http://127.0.0.1:8081，應顯示地圖和10個停車場標記，點擊任一標記，應彈出泡泡顯示該停車場的最新資料（包含名稱、地址、總車位、剩餘車位、更新時間）。

### Implementation for User Story 1

- [X] T009 [US1] Create Flask app instance and basic route structure in app.py
- [X] T010 [US1] Implement GET /api/parking/list endpoint in app.py to return all parking lots for dropdown
- [X] T011 [US1] Implement GET /api/parking/<id>/latest endpoint in app.py to return latest parking record
- [X] T044 [US1] Remove dropdown select element from templates/index.html
- [X] T045 [US1] Add Leaflet.js CSS and JavaScript CDN links to templates/index.html head section
- [X] T046 [US1] Create map container div in templates/index.html with id="map" and full viewport height/width styling
- [X] T047 [US1] Initialize Leaflet map in templates/index.html JavaScript with center at Taichung city (24.15, 120.67) and zoom level 12
- [X] T048 [US1] Fetch parking list from /api/parking/list on page load in templates/index.html
- [X] T049 [US1] Create Leaflet markers for each parking lot using lon/lat coordinates in templates/index.html
- [X] T050 [US1] Add markers to map and store marker references in JavaScript array in templates/index.html
- [X] T051 [US1] Calculate map bounds from all parking lot coordinates and fit map view to show all markers in templates/index.html
- [X] T052 [US1] Add click event handler to each marker to fetch latest data from /api/parking/<id>/latest in templates/index.html
- [X] T053 [US1] Create popup content with parking lot information (name, address, tot_space, empty_space, update_time) in templates/index.html
- [X] T054 [US1] Bind popup to marker and open popup when marker is clicked in templates/index.html
- [X] T055 [US1] Add download button in popup content that triggers CSV download via /api/parking/<id>/download in templates/index.html
- [X] T056 [US1] Add error handling for map initialization and API failures in templates/index.html JavaScript
- [X] T057 [US1] Add loading indicator while fetching parking list data in templates/index.html
- [X] T058 [US1] Style map container and popup content with CSS for readable layout in templates/index.html

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. User can open webpage, see map with 10 markers, click any marker to see popup with parking lot information and download button.

---

## Phase 4: User Story 2 - 下載歷史資料 (Priority: P2)

**Goal**: 企劃人員可以下載指定停車場的歷史累積資料（CSV格式）。

**Independent Test**: 點擊地圖標記後，在資訊泡泡中點擊下載按鈕，應能下載包含該停車場所有歷史記錄的CSV檔案，格式正確可用Excel開啟。

### Implementation for User Story 2

- [X] T018 [US2] Implement GET /api/parking/<id>/download endpoint in app.py to query all historical records and return CSV
- [X] T019 [US2] Add CSV generation logic in app.py download endpoint (include headers: id, name, address, tot_space, empty_space, update_time, lon, lat, recorded_at)
- [X] T020 [US2] Add Content-Disposition header in download endpoint with filename format: parking_<id>_<timestamp>.csv
- [X] T059 [US2] Integrate download button functionality into popup content in templates/index.html (replaces previous download button implementation)
- [X] T060 [US2] Add click event handler for download button in popup that calls /api/parking/<id>/download in templates/index.html
- [X] T061 [US2] Add error handling for download failures in popup in templates/index.html

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. User can view parking lot data on map and download historical data from popup.

---

## Phase 5: Scheduling & Data Collection

**Purpose**: Implement automatic data fetching every 10 minutes with deduplication

- [X] T024 Setup APScheduler in app.py to run background scheduler
- [X] T025 Create fetch_and_store_data() function in app.py that calls modified parking_api_taichung.py and stores results
- [X] T038 Update APScheduler job configuration in app.py to change interval from 30 minutes to 10 minutes
- [X] T039 Update scheduler startup message in app.py to reflect 10-minute interval
- [X] T027 Add error handling and logging in fetch_and_store_data() for failed API calls
- [X] T028 Trigger initial data fetch on app startup in app.py (optional: can be manual first run)

**Checkpoint**: System should automatically fetch and store parking data every 10 minutes, with deduplication based on update_time

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and edge case handling

- [X] T029 Add error handling for missing parking lot data in app.py API endpoints (return 404 with error message)
- [X] T062 Add handling for "no data yet" scenario in popup (show message when no records exist for parking lot) in templates/index.html
- [X] T063 Add loading indicator in popup while fetching latest data in templates/index.html
- [X] T032 Update README.md with new setup instructions for Flask app
- [X] T040 Update README.md to reflect 10-minute scheduling interval
- [X] T041 Add logging in store_parking_data() to show count of skipped duplicate records
- [X] T064 Update README.md to reflect map interface instead of dropdown
- [ ] T065 Test complete workflow: start app, wait for scheduled fetch, view map, click markers, verify popup displays correctly, download CSV

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - Map interface implementation
  - User Story 2 (Phase 4): Can start after Foundational, but needs US1's popup structure
  - Scheduling (Phase 5): Already complete
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses popup structure from US1 but independently testable

### Within Each User Story

- Map initialization before markers
- Markers creation before popup binding
- Popup content creation before event handlers
- Core implementation before error handling

### Parallel Opportunities

- **Phase 3 (US1)**:
  - T045-T046 can run in parallel (CSS and HTML structure)
  - T047-T051 can run in parallel (different parts of map initialization)
  - T052-T055 can run in parallel (different parts of popup functionality)
- **Phase 4 (US2)**:
  - T059-T061 can run in parallel (different parts of download integration)

---

## Parallel Example: User Story 1 - Map Implementation

```bash
# Launch map setup tasks in parallel:
Task: "Add Leaflet.js CSS and JavaScript CDN links to templates/index.html"
Task: "Create map container div in templates/index.html"

# Launch marker creation tasks in parallel:
Task: "Create Leaflet markers for each parking lot using lon/lat coordinates"
Task: "Calculate map bounds from all parking lot coordinates"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Map Interface)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Start Flask app: `python app.py`
   - Open browser, verify map loads with 10 markers
   - Click markers, verify popup displays correctly
   - Verify download button works in popup
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Map Interface) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Download in Popup) → Test independently → Deploy/Demo
4. Add Polish → Final testing → Deploy

### Manual Testing Checklist

After each phase, manually test:
- [ ] Flask app starts without errors
- [ ] Map loads correctly with Leaflet.js
- [ ] All 10 parking lot markers appear on map
- [ ] Map view automatically adjusts to show all markers
- [ ] Clicking marker shows popup with correct information
- [ ] Popup displays 5 required fields (name, address, tot_space, empty_space, update_time)
- [ ] Download button in popup works correctly
- [ ] CSV download contains correct data
- [ ] Error handling works for missing data
- [ ] Loading indicators display correctly

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All tasks include exact file paths for clarity
- No automated tests per project constitution - manual testing only
- **UI Change**: Replacing dropdown with map interface
- **Map Library**: Leaflet.js via CDN (no API key required)
- **Popup Content**: Only 5 fields (name, address, tot_space, empty_space, update_time)

---

## Summary

### Total Task Count

- **Phase 1**: 3 tasks (all completed)
- **Phase 2**: 9 tasks (all completed)
- **Phase 3 (US1 - Map Interface)**: 20 tasks (9 completed from previous, 11 new tasks T044-T058)
- **Phase 4 (US2 - Download)**: 6 tasks (3 completed, 3 new tasks T059-T061)
- **Phase 5**: 5 tasks (all completed)
- **Phase 6**: 8 tasks (5 completed, 3 new tasks T062-T065)

**Total**: 51 tasks
- **Completed**: 50 tasks (所有實作任務已完成)
- **Pending**: 1 task (T065 - 手動測試，需使用者執行)

### Key Changes from Previous Tasks

- **T044**: Remove dropdown (replaced by map)
- **T045-T058**: Map interface implementation (new)
- **T059-T061**: Download integration in popup (updated)
- **T062-T065**: Polish tasks for map interface (new/updated)
