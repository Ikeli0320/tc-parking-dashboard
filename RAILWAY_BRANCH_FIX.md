# Railway 部署問題修復 - 分支設定

## 問題診斷

Railway 錯誤訊息顯示只看到 `.gitignore`、`LICENSE`、`README.md`，這表示：

1. **Railway 可能連接到錯誤的分支**（`master` 而不是 `001-parking-dashboard`）
2. **`master` 分支沒有程式碼檔案**（已確認）

## 解決方案

### 步驟 1：在 Railway 設定正確的分支

1. 前往 Railway Dashboard
2. 進入專案設定（Settings）
3. 找到 **"Source"** 或 **"Repository"** 設定
4. 確認或修改以下設定：
   - **Branch**: 改為 `001-parking-dashboard`（不是 `master`）
   - **Root Directory**: 留空（使用根目錄）

### 步驟 2：確保所有檔案都已推送

執行以下命令確認並推送：

```bash
# 確認目前分支
git branch

# 確認檔案都在
git ls-files | grep -E "app.py|requirements.txt|Procfile|nixpacks.toml"

# 如果檔案有修改，提交並推送
git add .
git commit -m "Fix Railway deployment configuration"
git push origin 001-parking-dashboard
```

### 步驟 3：合併到 master 分支（可選）

如果你想讓 `master` 分支也有程式碼：

```bash
# 切換到 master
git checkout master

# 合併 001-parking-dashboard 分支
git merge 001-parking-dashboard

# 推送到 GitHub
git push origin master
```

然後在 Railway 設定中使用 `master` 分支。

### 步驟 4：重新部署

在 Railway Dashboard：
1. 確認分支設定正確
2. 點擊 **"Redeploy"** 或等待自動部署
3. 查看建置日誌確認是否成功

## 驗證清單

- [ ] Railway 分支設定為 `001-parking-dashboard`
- [ ] 所有檔案都已推送到 GitHub
- [ ] `nixpacks.toml` 存在且格式正確
- [ ] `requirements.txt` 存在
- [ ] `Procfile` 存在
- [ ] `app.py` 存在

## 如果仍然失敗

如果設定正確分支後仍然失敗，請檢查：

1. **建置日誌**：查看具體錯誤訊息
2. **檔案路徑**：確認 Railway 能正確讀取檔案
3. **Python 版本**：確認 `runtime.txt` 或 `nixpacks.toml` 中的版本正確

