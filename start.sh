#!/bin/bash
# Railway start script for parking dashboard

# 確保 data 目錄存在
mkdir -p data

# 啟動應用程式
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120

