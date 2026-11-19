import os
import secrets

_INSECURE_SECRET_KEYS = {
    "",
    "your-secret-key",
    "secret",
    "changeme",
    "change-me",
    "dev",
}

def _secret_key():
    """Use FLASK_SECRET_KEY. Production fails closed; dev gets a random key."""
    key = os.environ.get("FLASK_SECRET_KEY", "").strip()
    production = os.environ.get("FLASK_ENV", "").lower() == "production"
    if key.lower() not in _INSECURE_SECRET_KEYS and len(key) >= 32:
        return key
    if production:
        raise RuntimeError(
            "FLASK_SECRET_KEY must be a random string of at least 32 characters."
        )
    return secrets.token_hex(32)

class Config:
    """應用配置類"""
    # Flask 配置
    SECRET_KEY = _secret_key()
    
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