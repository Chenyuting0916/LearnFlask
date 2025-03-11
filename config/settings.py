import os

class Config:
    """應用配置類"""
    # Flask 配置
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key')
    
    # 數據目錄配置
    DATA_DIR = 'app/data'
    CACHE_DIR = 'cache'
    DEFAULT_VOCABULARY_FILE = os.path.join(DATA_DIR, 'default_vocabulary.json')
    VOCABULARY_CACHE_FILE = os.path.join(CACHE_DIR, 'vocabulary.json')
    
    # Jisho.org 配置
    JISHO_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    JISHO_TIMEOUT = 10  # 單一請求超時時間（秒）
    FETCH_TIMEOUT = 3   # 整體抓取超時時間（秒）
    MAX_WORDS = 200
    MAX_PAGES = 20 