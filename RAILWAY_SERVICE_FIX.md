# Railway 服務配置問題修復

## 問題
訪問 https://tc-parking-dashboard.railway.app/ 時顯示 Railway 預設 API 頁面，而不是應用程式。

## 原因
Railway 可能將服務配置為 Private Service 而不是 Public Web Service。

## 解決方案

### 在 Railway Dashboard 中：

1. **進入專案設定**
   - 前往 Railway Dashboard
   - 點擊專案 `tc-parking-dashboard`

2. **檢查服務設定**
   - 找到服務（Service）設定
   - 確認服務類型為 **Web Service**（不是 Private Service）

3. **生成公開 URL**
   - 在服務設定中找到 **"Generate Domain"** 或 **"Settings"** → **"Networking"**
   - 確保服務已設定為 **Public**（公開）
   - 如果沒有公開 URL，點擊 **"Generate Domain"** 建立一個

4. **檢查端口設定**
   - 確認 Railway 自動偵測到端口（應該會自動偵測）
   - 或者手動設定環境變數 `PORT`（但通常不需要）

5. **重新部署**
   - 如果修改了設定，可能需要重新部署
   - 點擊 **"Redeploy"**

## 驗證

部署成功後，訪問公開 URL 應該會看到：
- 地圖介面
- 10 個停車場標記
- 而不是 Railway 的預設 API 頁面

## 如果仍然失敗

如果修改設定後仍然顯示 Railway API 頁面，可能是：
1. 服務沒有正確暴露為 Web Service
2. 需要等待幾分鐘讓設定生效
3. 檢查 Railway 的日誌確認應用程式是否正常運行




