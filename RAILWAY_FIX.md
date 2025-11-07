# Railway 部署問題修復

## 問題
Railway 建置失敗：`Error creating build plan with Railpack`

## 解決方案
已建立以下配置檔案來明確指定建置步驟：

### 1. `nixpacks.toml` ✅
明確指定建置步驟和啟動命令

### 2. `railway.json` ✅
Railway 專用配置檔案

### 3. `Procfile` ✅
已存在，指定啟動命令

### 4. `requirements.txt` ✅
已存在，包含所有依賴

### 5. `runtime.txt` ✅
已存在，指定 Python 版本

## 下一步

1. **提交並推送這些新檔案到 GitHub**：
   ```bash
   git add nixpacks.toml railway.json
   git commit -m "Add Railway deployment configuration"
   git push origin 001-parking-dashboard
   ```

2. **在 Railway 重新部署**：
   - Railway 會自動偵測新的配置檔案
   - 重新觸發部署（如果沒有自動觸發，可以手動點擊 "Redeploy"）

3. **檢查建置日誌**：
   - 如果還有問題，查看 Railway 的建置日誌
   - 確認所有依賴都正確安裝

## 如果仍然失敗

### 選項 1：使用 Dockerfile（備選方案）
如果 Nixpacks 仍有問題，可以建立 Dockerfile：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "2"]
```

### 選項 2：檢查 Railway 設定
在 Railway Dashboard：
1. 進入專案設定
2. 確認 "Build Command" 為空（使用 nixpacks.toml）
3. 確認 "Start Command" 為空（使用 nixpacks.toml）

### 選項 3：使用其他平台
如果 Railway 持續有問題，可以考慮：
- **Render** - 更簡單的配置
- **Fly.io** - 需要 Dockerfile
- **PythonAnywhere** - 手動部署

