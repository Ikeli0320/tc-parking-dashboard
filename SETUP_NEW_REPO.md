# 建立新的 GitHub Repository 步驟

## 步驟 1：在 GitHub 建立新 Repository

1. 前往 https://github.com/new
2. 填寫以下資訊：
   - **Repository name**: `parking-dashboard`
   - **Description**: `台中市停車場資料爬蟲與查詢站台`
   - **Visibility**: 選擇 **Public** ✅
   - **不要**勾選 "Initialize this repository with a README"（因為本地已有專案）
   - **不要**勾選 "Add .gitignore"（本地已有）
   - **不要**選擇 License（或選擇適合的授權）
3. 點擊 **Create repository**

## 步驟 2：連接本地專案到新 Repository

建立 repository 後，GitHub 會顯示設定指令。執行以下命令：

```bash
# 新增新的 remote（將 YOUR_USERNAME 和 REPO_NAME 替換為你的實際值）
git remote add origin https://github.com/Ikeli0320/tc-parking-dashboard.git
git@github.com:Ikeli0320/tc-parking-dashboard.git

# 例如：
# git remote add origin https://github.com/Ikeli0320/Crawl-ike.git

# 確認 remote 設定
git remote -v

# 推送所有分支到新 repository
git push -u origin 001-parking-dashboard
git push -u origin master
```

## 步驟 3：驗證

1. 前往你的新 GitHub repository 頁面
2. 確認所有檔案都已上傳
3. 確認分支 `001-parking-dashboard` 和 `master` 都存在

## 注意事項

- 確保 `.gitignore` 已正確設定（避免上傳敏感資料）
- `data/parking.db` 已在 `.gitignore` 中，不會被上傳
- `venv/` 目錄也不會被上傳

