import os
import json
from typing import List, Any
from config.settings import Config

class Cache:
    """快取管理工具"""
    
    def __init__(self):
        """初始化快取，確保快取目錄存在"""
        os.makedirs(Config.CACHE_DIR, exist_ok=True)
    
    def save(self, data: List[Any], filename: str) -> None:
        """保存數據到快取文件"""
        try:
            filepath = os.path.join(Config.CACHE_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving cache: {e}")
    
    def load(self, filename: str) -> List[Any]:
        """從快取文件加載數據"""
        return self.load_from_path(os.path.join(Config.CACHE_DIR, filename))
    
    def load_from_path(self, filepath: str) -> List[Any]:
        """從指定路徑加載 JSON 數據"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading file {filepath}: {e}")
        return []
    
    def clear(self, filename: str) -> None:
        """清除快取文件"""
        try:
            filepath = os.path.join(Config.CACHE_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        except IOError as e:
            print(f"Error clearing cache: {e}") 