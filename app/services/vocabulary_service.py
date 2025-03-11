from typing import List, Optional
from app.models.vocabulary import Word
from app.services.jisho_service import JishoService
from app.utils.cache import Cache
from config.settings import Config
import random

class VocabularyService:
    """詞彙管理服務"""
    
    def __init__(self):
        self._jisho_service = JishoService()
        self._cache = Cache()
        self.vocabulary: List[Word] = []
        self.learned_words: List[int] = []  # 新增：用於儲存已學習的單字索引
        self.load_vocabulary()
        
    def load_vocabulary(self) -> None:
        """從快取或網路加載詞彙"""
        # 嘗試從快取加載
        cached_words = self._cache.load('vocabulary.json')
        if cached_words:
            self.vocabulary = [Word(**word) for word in cached_words]
            # 嘗試加載已學習的單字
            learned = self._cache.load('learned_words.json')
            if learned:
                self.learned_words = learned
            return
            
        # 嘗試從網路加載
        words = self._jisho_service.fetch_n1_words()
        if words:
            # 設置正確的ID
            for i, word in enumerate(words):
                word.id = i
            self.vocabulary = words
            self._cache.save([vars(word) for word in words], 'vocabulary.json')
            self._cache.save([], 'learned_words.json')  # 初始化空的已學習單字列表
            return
            
        # 如果都失敗了，使用默認詞彙
        self.vocabulary = self._load_default_vocabulary()
        self._cache.save([vars(word) for word in self.vocabulary], 'vocabulary.json')
        self._cache.save([], 'learned_words.json')
            
    def refresh(self) -> int:
        """重新從網路加載詞彙"""
        words = self._jisho_service.fetch_n1_words()
        if not words:
            words = self._load_default_vocabulary()
            
        # 隨機打亂單字順序
        random.shuffle(words)
            
        # 設置正確的ID
        for i, word in enumerate(words):
            word.id = i
            
        self.vocabulary = words
        self.learned_words = []  # 重置已學習的單字
        self._cache.save([vars(word) for word in words], 'vocabulary.json')
        self._cache.save([], 'learned_words.json')
        return len(words)
        
    def add_learned_word(self, index: int) -> None:
        """新增已學習的單字"""
        if index not in self.learned_words and 0 <= index < len(self.vocabulary):
            self.learned_words.append(index)
            self._cache.save(self.learned_words, 'learned_words.json')
            
    def get_learned_words(self) -> List[Word]:
        """獲取已學習的單字列表"""
        return [self.vocabulary[i] for i in self.learned_words]
        
    def get_word(self, index: int) -> Optional[Word]:
        """獲取指定索引的單字"""
        if 0 <= index < len(self.vocabulary):
            return self.vocabulary[index]
        return None
            
    def get_words(self, indices: List[int]) -> List[Word]:
        """獲取多個詞彙"""
        return [self.vocabulary[i] for i in indices if 0 <= i < len(self.vocabulary)]
        
    def _load_default_vocabulary(self) -> List[Word]:
        """從默認文件加載詞彙"""
        try:
            default_words = self._cache.load_from_path(Config.DEFAULT_VOCABULARY_FILE)
            return [Word(**word) for word in default_words]
        except Exception as e:
            print(f"Error loading default vocabulary: {e}")
            return [] 