# Railway 部署問題 - 使用 Dockerfile

## 問題
Railway 的 Railpack 無法偵測到專案檔案，只看到 `.gitignore`、`LICENSE`、`README.md`。

## 解決方案
已建立 `Dockerfile` 並將 Railway 設定改為使用 Docker 建置器，而不是 Railpack。

## 已完成的變更

1. **建立 `Dockerfile`** ✅
   - 使用 Python 3.11-slim 基礎映像
   - 安裝所有依賴套件
   - 複製應用程式檔案
   - 設定啟動命令

2. **更新 `railway.toml`** ✅
   - 將 builder 從 `nixpacks` 改為 `dockerfile`

## 下一步

1. **在 Railway Dashboard 確認設定**：
   - 進入專案設定（Settings）
   - 確認 Branch 為 `main`
   - 確認 Build Command 為空（使用 Dockerfile）
   - 確認 Start Command 為空（使用 Dockerfile 中的 CMD）

2. **重新部署**：
   - Railway 會自動偵測到 `Dockerfile`
   - 使用 Docker 建置器進行建置
   - 應該能正確偵測到所有檔案

## 如果仍然失敗

### 選項 1：檢查 Railway 設定
- 確認 Root Directory 為空（使用根目錄）
- 確認沒有設定 Build Command（讓 Dockerfile 處理）

### 選項 2：手動指定建置器
在 Railway Dashboard 的 Settings 中：
- Build Command: 留空
- Start Command: 留空
- 讓 Railway 自動偵測 Dockerfile

### 選項 3：使用其他平台
如果 Railway 持續有問題，可以考慮：
- **Render** - 更簡單的配置
- **Fly.io** - 原生支援 Dockerfile
- **PythonAnywhere** - 手動部署

## Dockerfile 說明

Dockerfile 會：
1. 使用 Python 3.11-slim 作為基礎映像
2. 安裝系統依賴（gcc，用於編譯某些 Python 套件）
3. 安裝所有 Python 依賴（從 requirements.txt）
4. 複製所有應用程式檔案
5. 建立 data 目錄（用於 SQLite）
6. 使用 gunicorn 啟動應用程式

## 驗證

部署成功後，應該能看到：
- 建置階段成功完成
- 應用程式正常啟動
- 可以訪問網頁介面

