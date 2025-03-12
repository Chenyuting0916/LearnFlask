# 日本語N1単語学習 / Japanese N1 Vocabulary Learning

一個簡單的日語N1單字學習網站，使用 Flask 框架開發。
A simple Japanese N1 vocabulary learning website built with Flask.

## Live Demo 線上演示 在线演示

Visit the live website at: [https://cyt.pythonanywhere.com](https://cyt.pythonanywhere.com)

## 功能特點 / Features

- 從 Jisho.org 自動抓取 N1 單字 / Automatically fetches N1 vocabulary from Jisho.org
- 支持顯示/隱藏單字含義 / Show/hide word meanings
- 記錄已學習的單字 / Track learned words
- 支持重新載入單字庫 / Reload vocabulary database
- 響應式設計，支持手機瀏覽 / Responsive design for mobile devices


## 技術棧 / Tech Stack

- Python 3.10+
- Flask
- BeautifulSoup4
- HTML5/CSS3/JavaScript

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

4. 運行應用 / Run the application:
```bash
python app.py
```

## 部署 / Deployment

### 本地部署 / Local Deployment

1. 確保已安裝 Python 3.10 或更高版本 / Ensure Python 3.10+ is installed
2. 按照安裝步驟設置環境 / Follow installation steps
3. 運行 `python app.py` / Run `python app.py`
4. 訪問 `http://localhost:5000` / Visit `http://localhost:5000`

### PythonAnywhere 部署 / PythonAnywhere Deployment

1. 在 PythonAnywhere 創建一個新的 Web 應用 / Create a new Web app on PythonAnywhere
2. 選擇 Flask 框架 / Choose Flask framework
3. 設置 Python 版本為 3.10 / Set Python version to 3.10
4. 上傳代碼到 PythonAnywhere / Upload code to PythonAnywhere
5. 設置虛擬環境並安裝依賴 / Set up virtual environment and install dependencies
6. 配置 WSGI 文件 / Configure WSGI file
7. 重新加載應用 / Reload the application

### GitHub Actions 自動部署 / GitHub Actions Auto Deployment

1. 在 GitHub 倉庫設置中添加以下 Secrets / Add the following Secrets to GitHub repository settings:
   - `PA_USERNAME`: PythonAnywhere 用戶名 / PythonAnywhere username
   - `PA_API_TOKEN`: PythonAnywhere API Token

2. 推送代碼到 main 分支時會自動部署 / Code will be automatically deployed when pushed to main branch

## 使用說明 / Usage

1. 打開網站後會顯示一個隨機的 N1 單字 / A random N1 word will be displayed when you open the website
2. 點擊「顯示含義」按鈕查看單字的中文含義 / Click "Show Meaning" to view the word's meaning
3. 點擊「下一個單字」按鈕學習下一個單字 / Click "Next Word" to learn the next word
4. 點擊「重新載入單字庫」可以重新獲取新的單字 / Click "Reload Vocabulary" to fetch new words
5. 右側面板顯示已學習的單字列表 / Learned words are displayed in the right panel

## 注意事項 / Notes

- 首次運行時會從 Jisho.org 抓取單字，可能需要一些時間 / First run will fetch words from Jisho.org, which may take some time
- 如果抓取失敗，會使用默認的單字庫 / If fetching fails, default vocabulary will be used
- 建議使用現代瀏覽器訪問 / Modern browsers are recommended

## 貢獻 / Contributing

歡迎提交 Issue 和 Pull Request！
Feel free to submit issues and pull requests!

## 授權 / License

MIT License
