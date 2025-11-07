# 部署指南：免費平台部署選項

本專案是一個 Flask 應用程式，包含背景排程任務（每10分鐘執行一次）和 SQLite 資料庫。以下是適合的免費部署平台推薦。

## 🎯 推薦平台（按優先順序）

### 1. **Railway** ⭐ 最推薦
- **免費額度**：每月 $5 免費額度（約 500 小時運行時間）
- **優點**：
  - 支援背景任務（APScheduler）
  - 自動部署（連接 GitHub）
  - 支援 SQLite 檔案系統
  - 簡單易用
  - 提供 HTTPS
- **缺點**：免費額度有限，可能需要升級
- **適合**：個人專案、測試環境

**部署步驟**：
1. 註冊 Railway：https://railway.app
2. 連接 GitHub 倉庫
3. 選擇「Deploy from GitHub repo」
4. Railway 會自動偵測 Python 專案
5. 設定環境變數（如需要）
6. 部署完成後會自動提供 URL

---

### 2. **Render** ⭐ 推薦
- **免費額度**：免費層可用，但應用會在 15 分鐘無活動後休眠
- **優點**：
  - 支援背景任務
  - 自動部署
  - 提供 HTTPS
  - 簡單設定
- **缺點**：
  - 免費層會休眠（首次訪問需要喚醒）
  - 排程任務可能受影響
- **適合**：低流量專案

**部署步驟**：
1. 註冊 Render：https://render.com
2. 建立新的 Web Service
3. 連接 GitHub 倉庫
4. 設定 Build Command：`pip install -r requirements.txt`
5. 設定 Start Command：`gunicorn app:app --bind 0.0.0.0:$PORT`
6. 部署

---

### 3. **PythonAnywhere** ⭐ 推薦（適合 Python 專案）
- **免費額度**：免費帳號可用
- **優點**：
  - 專為 Python 設計
  - 支援背景任務（可設定排程）
  - 提供免費子網域
  - 簡單易用
- **缺點**：
  - 免費帳號有限制（只能從白名單網站存取）
  - 需要手動設定
- **適合**：Python 專案、學習用途

**部署步驟**：
1. 註冊 PythonAnywhere：https://www.pythonanywhere.com
2. 上傳專案檔案
3. 設定 Web App
4. 設定排程任務（Tasks）
5. 部署

---

### 4. **Fly.io** ⭐ 推薦
- **免費額度**：每月 3 個共享 CPU 虛擬機，160GB 出站流量
- **優點**：
  - 支援背景任務
  - 全球 CDN
  - 提供 HTTPS
  - 支援 SQLite
- **缺點**：設定較複雜
- **適合**：需要全球部署的專案

**部署步驟**：
1. 註冊 Fly.io：https://fly.io
2. 安裝 flyctl CLI
3. 執行 `fly launch`
4. 部署

---

### 5. **Replit** 
- **免費額度**：免費可用
- **優點**：
  - 線上 IDE
  - 簡單部署
  - 提供 HTTPS
- **缺點**：
  - 免費層有限制
  - 背景任務可能不穩定
- **適合**：快速測試、學習

---

## 📋 部署前準備

### 1. 建立部署配置檔案

專案已包含以下配置檔案：
- `Procfile` - 用於 Railway/Render
- `runtime.txt` - 指定 Python 版本
- `gunicorn` - 生產環境 WSGI 伺服器（已加入 requirements.txt）

### 2. 修改應用程式設定

部署時需要修改 `app.py` 的啟動方式：

```python
# 生產環境使用 gunicorn，開發環境使用 Flask 內建伺服器
if __name__ == '__main__':
    # 開發模式
    fetch_and_store_data()
    app.run(debug=True, host='0.0.0.0', port=8081)
```

生產環境會使用 `gunicorn` 啟動（見 Procfile）。

### 3. 環境變數設定

某些平台可能需要設定環境變數：
- `PORT` - 應用程式監聽的端口（多數平台會自動設定）

---

## 🚀 快速部署（Railway 範例）

### 步驟 1：準備專案

確保專案已推送到 GitHub。

### 步驟 2：連接 Railway

1. 前往 https://railway.app
2. 點擊 "Login" 並使用 GitHub 登入
3. 點擊 "New Project"
4. 選擇 "Deploy from GitHub repo"
5. 選擇你的倉庫

### 步驟 3：設定部署

Railway 會自動偵測 Python 專案並使用 `Procfile`。

### 步驟 4：取得 URL

部署完成後，Railway 會提供一個 URL（例如：`https://your-app.railway.app`）

---

## ⚠️ 注意事項

### SQLite 資料庫

- **檔案系統持久化**：某些平台（如 Render 免費層）的檔案系統是暫時的，重啟後資料會消失
- **解決方案**：
  1. 使用外部資料庫（如 PostgreSQL，但需要付費或使用免費服務）
  2. 定期備份資料庫
  3. 使用有持久化儲存的平台（如 Railway）

### 背景排程任務

- **確保平台支援背景任務**：不是所有平台都支援持續運行的背景任務
- **免費層限制**：某些平台的免費層會讓應用休眠，可能影響排程執行

### 資源限制

- **記憶體限制**：免費層通常有記憶體限制
- **CPU 限制**：免費層可能有 CPU 使用限制
- **流量限制**：注意免費額度的流量限制

---

## 🔧 平台特定設定

### Railway

建立 `railway.json`（可選）：
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Render

在 Render Dashboard 設定：
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### PythonAnywhere

1. 上傳專案檔案
2. 在 Web 標籤設定 WSGI 檔案
3. 在 Tasks 標籤設定排程任務（每10分鐘執行一次）

---

## 📊 平台比較表

| 平台 | 免費額度 | 背景任務 | SQLite 支援 | 自動部署 | 難易度 |
|------|---------|---------|------------|---------|--------|
| Railway | $5/月 | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Render | 免費層 | ⚠️（會休眠） | ⚠️ | ✅ | ⭐⭐⭐⭐ |
| PythonAnywhere | 免費 | ✅ | ✅ | ❌ | ⭐⭐⭐ |
| Fly.io | 3 VM/月 | ✅ | ✅ | ✅ | ⭐⭐⭐ |
| Replit | 免費 | ⚠️ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |

---

## 🎓 推薦選擇

**最佳選擇**：**Railway**
- 最適合這個專案
- 支援背景任務和 SQLite
- 簡單易用
- 免費額度足夠個人專案使用

**備選方案**：
- **Render**：如果 Railway 額度用完
- **PythonAnywhere**：如果需要更多控制權

---

## 📝 部署後檢查清單

- [ ] 應用程式可以正常訪問
- [ ] 地圖可以正常載入
- [ ] 標記可以正常顯示
- [ ] 點擊標記可以顯示資訊泡泡
- [ ] 下載功能正常
- [ ] 排程任務正常執行（等待10分鐘後檢查資料是否更新）
- [ ] HTTPS 正常運作

---

## 🆘 常見問題

### Q: 部署後應用無法啟動？
A: 檢查：
1. `requirements.txt` 是否包含所有依賴
2. `Procfile` 是否正確
3. 日誌中的錯誤訊息

### Q: 排程任務沒有執行？
A: 檢查：
1. 平台是否支援背景任務
2. 應用是否持續運行（沒有休眠）
3. 日誌中是否有錯誤

### Q: 資料庫資料消失？
A: 某些平台的檔案系統是暫時的，需要：
1. 使用有持久化儲存的平台
2. 或定期備份資料庫

---

## 🔗 相關連結

- [Railway 文件](https://docs.railway.app)
- [Render 文件](https://render.com/docs)
- [PythonAnywhere 文件](https://help.pythonanywhere.com)
- [Fly.io 文件](https://fly.io/docs)

