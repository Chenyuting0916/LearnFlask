# 日本語学習平台 / Japanese Learning Platform

一個全面的日語學習平台，提供假名、單字、測驗等多種學習功能。
A comprehensive Japanese learning platform offering hiragana, vocabulary, quizzes and more.

## 線上演示 / Live Demo

訪問網站：[https://cyt.pythonanywhere.com](https://cyt.pythonanywhere.com)

## 功能特點 / Features

### 基礎學習 / Basic Learning
- 平假名和片假名練習 / Hiragana and Katakana practice
- 基礎單字學習 / Basic vocabulary learning
- 自動記錄學習進度 / Automatic progress tracking

### 進階功能 / Advanced Features
- 專業測驗系統（付費會員） / Professional quiz system (paid members)
- 個人化學習記錄 / Personalized learning history
- 詳細的學習統計 / Detailed learning statistics

### 技術特點 / Technical Features
- 響應式設計，支持各種設備 / Responsive design for all devices
- 數據自動同步 / Automatic data synchronization
- 安全的用戶認證系統 / Secure user authentication system


## 技術棧 / Tech Stack

### 後端 / Backend
- Python 3.10+
- Flask 3.0.2
- Werkzeug 3.0.1
- Jinja2 3.1.3

### 前端 / Frontend
- HTML5/CSS3/JavaScript
- Bootstrap 5
- jQuery

### 工具和依賴 / Tools & Dependencies
- BeautifulSoup4 4.12.3
- Requests 2.31.0
- WTForms 3.1.2
- Gunicorn 21.2.0

## 安裝步驟 / Installation

1. 克隆專案 / Clone the repository:
```bash
git clone https://github.com/yourusername/learnflask.git
cd learnflask
```

2. 創建並啟動虛擬環境 / Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安裝依賴 / Install dependencies:
```bash
pip install -r requirements.txt
```

4. 初始化數據目錄 / Initialize data directories:
```bash
mkdir -p app/data cache
```

5. 運行應用 / Run the application:
```bash
python app.py
```

## 部署 / Deployment

### 本地部署 / Local Deployment
1. 確保已安裝 Python 3.10+ / Ensure Python 3.10+ is installed
2. 按照安裝步驟設置環境 / Follow installation steps
3. 運行 `python app.py` / Run `python app.py`
4. 訪問 `http://localhost:5000` / Visit `http://localhost:5000`

### PythonAnywhere 部署 / PythonAnywhere Deployment
1. 在 PythonAnywhere 創建 Web 應用 / Create a Web app on PythonAnywhere
2. 選擇 Flask 框架和 Python 3.10 / Choose Flask framework and Python 3.10
3. 設置以下環境變量 / Set the following environment variables:
   - `FLASK_ENV`: `production`
   - `FLASK_SECRET_KEY`: `your-secret-key`

### GitHub Actions 自動部署 / GitHub Actions Auto Deployment
配置以下 Secrets / Configure the following Secrets:
- `PA_USERNAME`: PythonAnywhere 用戶名 / PythonAnywhere username
- `PA_API_TOKEN`: PythonAnywhere API Token

## 開發指南 / Development Guide

### 代碼結構 / Code Structure
```
learnflask/
├── app/
│   ├── data/          # 學習資源數據
│   ├── routes/        # 路由處理
│   ├── services/      # 業務邏輯
│   ├── static/        # 靜態文件
│   └── templates/     # 模板文件
├── cache/             # 緩存文件
├── config/           # 配置文件
├── tests/           # 測試文件
└── requirements.txt  # 依賴清單
```

### 添加新功能 / Adding New Features
1. 在相應目錄創建新文件 / Create new files in appropriate directories
2. 更新路由和服務 / Update routes and services
3. 添加測試用例 / Add test cases
4. 更新文檔 / Update documentation

## 貢獻指南 / Contributing

歡迎提交 Issue 和 Pull Request！在提交之前，請：
1. 檢查現有的 Issue 和 PR
2. 遵循代碼風格指南
3. 添加適當的測試
4. 更新相關文檔

## 授權 / License

MIT License
