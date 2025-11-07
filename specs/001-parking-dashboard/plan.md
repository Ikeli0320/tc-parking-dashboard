# Implementation Plan: 停車場資料查詢站台（地圖介面更新）

**Branch**: `001-parking-dashboard` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-parking-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

將首頁從下拉選單改為地圖介面，讓企劃人員可以在地圖上看到10個停車場的位置標記，點擊標記後彈出資訊泡泡顯示即時資料（名稱、地址、總車位、剩餘車位、更新時間），並提供下載歷史資料的按鈕。採用最簡單的地圖解決方案：Leaflet.js（開源，無需API key，立即可用）。

## Technical Context

**Language/Version**: Python 3.9+ (與現有程式一致)

**Primary Dependencies**: 
- Flask (輕量級 Web 框架，最簡單快速)
- SQLite3 (內建，無需額外安裝)
- APScheduler (排程任務，每10分鐘執行)
- Leaflet.js (開源地圖庫，CDN載入，無需API key)
- 現有的 requests, beautifulsoup4, pandas (沿用)

**Storage**: SQLite 資料庫檔案 (單一檔案，易於部署)

**Testing**: 手動測試 (符合專案憲法：不建立自動化測試套件)

**Target Platform**: Web 瀏覽器 (桌面和行動裝置)

**Project Type**: web (簡單的前後端整合)

**Performance Goals**: 
- 網頁載入時間 < 3秒（包含地圖載入）
- 地圖標記點擊回應時間 < 200ms
- 資訊泡泡顯示時間 < 100ms
- 排程執行時間 < 1分鐘（10個停車場）
- 資料去重檢查時間 < 100ms per record

**Constraints**: 
- 無需帳密驗證
- 必須使用現有的 `parking_api_taichung.py` 程式邏輯
- 地圖必須能容納10個停車場位置（台中市範圍）
- 地圖庫必須無需API key，立即可用
- 必須能在標準 Python 環境中直接執行
- 排程頻率：每10分鐘執行一次

**Scale/Scope**: 
- 10個指定停車場
- 單一使用者或少量同時使用者
- 地圖顯示範圍：台中市（需自動調整視角以包含所有10個地點）
- 資料累積速度：每10分鐘10筆記錄（如果資料有更新）
- 資料去重：基於 update_time 欄位檢查重複

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Check ✅

**Minimal Scope Principle**: ✅ 符合
- 僅實作地圖顯示、標記點擊、資訊泡泡三個核心功能
- 使用最簡單的地圖庫（Leaflet.js），無架構性設計
- 資訊泡泡僅顯示必要的5個欄位

**Rapid Delivery Principle**: ✅ 符合
- 選擇 Leaflet.js（開源，CDN載入，無需API key）
- 使用現有的 API 端點，無需修改後端
- 簡單的 HTML/JavaScript 前端，無需建置工具

**Immediate Executability Principle**: ✅ 符合
- Leaflet.js 透過 CDN 載入，無需額外安裝
- 無需 API key 或複雜設定
- 可在標準環境中直接執行

**Documentation Simplicity Principle**: ✅ 符合
- 僅提供啟動指令和使用說明
- 無需詳細的架構文件

**Scope Boundaries**: ✅ 符合
- 不建立可擴充架構
- 不進行效能優化（除非影響基本功能）
- 不建立自動化測試
- 不建立 CI/CD
- 不進行程式碼重構

### Post-Design Check ✅

**Minimal Scope Principle**: ✅ 仍然符合
- 地圖介面僅包含必要的標記和資訊泡泡
- 資訊泡泡僅顯示5個必要欄位（名稱、地址、總車位、剩餘車位、更新時間）
- 無額外的地圖功能（如路線規劃、搜尋、縮放控制等進階功能）
- 使用最簡單的 Leaflet.js，無需複雜設定

**Rapid Delivery Principle**: ✅ 仍然符合
- Leaflet.js 是最簡單的開源地圖解決方案
- 使用 CDN 載入，無需建置流程
- 前端邏輯簡單直接（標記、點擊、資訊泡泡）
- 無需修改後端 API

**Immediate Executability Principle**: ✅ 仍然符合
- 地圖透過 CDN 載入，無需額外設定
- 無需 API key 或註冊
- 可在標準環境中直接執行
- 瀏覽器直接支援，無需額外插件

**Documentation Simplicity Principle**: ✅ 仍然符合
- quickstart.md 僅包含必要的啟動和使用說明
- 無詳細的架構圖或複雜的技術文件
- 地圖使用說明簡潔明瞭

**Scope Boundaries**: ✅ 仍然符合
- 所有設計都在必要範圍內
- 無違規的擴充設計
- 地圖功能僅限於顯示標記和資訊泡泡，無其他進階功能

## Project Structure

### Documentation (this feature)

```text
specs/001-parking-dashboard/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app.py                   # Flask 主程式（整合爬蟲、API、排程）
parking_api_taichung.py  # 現有爬蟲程式（修改為可被呼叫的模組）
templates/
└── index.html           # 前端頁面（地圖介面、標記、資訊泡泡、下載按鈕）
static/                  # 靜態檔案（CSS、JS，如果需要）
data/
└── parking.db           # SQLite 資料庫（自動建立）
output/                  # 現有輸出目錄（保留）
```

**Structure Decision**: 採用最簡單的單一檔案結構。`app.py` 包含所有後端邏輯（Flask routes、資料庫操作、排程），`parking_api_taichung.py` 修改為可被匯入的模組。前端使用單一 HTML 檔案，內嵌 JavaScript，使用 Leaflet.js CDN，無需建置工具。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

無違規項目。

## Changes from Previous Plan

### UI 改進需求

1. **介面變更**：
   - 原：下拉選單選擇停車場
   - 新：地圖介面顯示10個停車場位置標記
   - 影響：需要重新設計前端頁面

2. **互動方式變更**：
   - 原：選擇下拉選單項目後顯示資料
   - 新：點擊地圖標記後彈出資訊泡泡
   - 影響：需要實作地圖標記和資訊泡泡功能

3. **資訊顯示變更**：
   - 原：顯示完整資訊（包含經緯度）
   - 新：資訊泡泡僅顯示5個欄位（名稱、地址、總車位、剩餘車位、更新時間）
   - 影響：簡化資訊泡泡內容

4. **下載功能整合**：
   - 原：在資訊顯示區域有下載按鈕
   - 新：在資訊泡泡中提供下載按鈕
   - 影響：下載按鈕需整合到資訊泡泡中

### Implementation Impact

- **templates/index.html**: 
  - 移除下拉選單
  - 加入 Leaflet.js 地圖
  - 實作地圖標記（10個停車場位置）
  - 實作資訊泡泡（點擊標記顯示）
  - 在資訊泡泡中加入下載按鈕
  - 自動調整地圖視角以包含所有10個地點

- **app.py**: 
  - 無需修改（現有 API 端點已足夠）

- **API 端點**: 
  - 無需新增（使用現有的 `/api/parking/list` 和 `/api/parking/<id>/latest`）
