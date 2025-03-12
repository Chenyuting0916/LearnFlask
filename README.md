# Japanese Vocabulary Learning Website

A web application to help you learn Japanese JLPT N1 vocabulary. The app automatically fetches words from Jisho.org and provides an interactive interface for learning.

## Live Demo 線上演示 在线演示

Visit the live website at: [https://cyt.pythonanywhere.com](https://cyt.pythonanywhere.com)

## Features 機能 功能

- 🔄 Automatically fetches JLPT N1 vocabulary from Jisho.org
- 📝 Shows Japanese words with their readings and meanings
- ✅ Tracks learned words
- 🎯 Focuses on 50 words at a time for effective learning
- 🔍 Random word selection from different pages for variety
- 💾 Caches vocabulary for offline access
- 🌐 Deployed on PythonAnywhere for 24/7 access
- 🔄 Automatic deployment with GitHub Actions

## Setup 設定 設置

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage 使用方法 使用方式

1. Click "Show Meaning" to reveal the meaning of the current word
2. Click "Next Word" to move to the next word
3. Click "Update Words" to fetch 50 new words from Jisho.org
4. Previously learned words are displayed below

## Deployment 部署 部署

The application is automatically deployed to PythonAnywhere using GitHub Actions:

1. Push changes to the main branch
2. GitHub Actions will:
   - Run tests
   - Trigger a reload on PythonAnywhere
3. Changes will be live in seconds

## Development 開發 开发

- Built with Flask
- Uses BeautifulSoup4 for web scraping
- Caches data locally for better performance
- Follows Python best practices

## Contributing 貢獻 贡献

Feel free to submit issues and enhancement requests!
