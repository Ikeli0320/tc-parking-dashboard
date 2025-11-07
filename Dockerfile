# 使用 Python 3.11 作為基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（如果需要）
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 複製所有應用程式檔案
COPY . .

# 建立 data 目錄（用於 SQLite 資料庫）
RUN mkdir -p data

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PORT=8081

# 暴露端口（Railway 會自動設定 PORT 環境變數，使用預設值）
EXPOSE 8081

# 啟動應用程式（使用環境變數 PORT，如果沒有則使用 8081）
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8081} --workers 2 --timeout 120

