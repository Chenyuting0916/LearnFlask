import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from app.models.vocabulary import Word
from config.settings import Config

class JishoService:
    """Jisho.org 網站爬蟲服務"""
    
    def __init__(self):
        self.headers = {'User-Agent': Config.JISHO_USER_AGENT}
    
    def fetch_n1_words(self, max_words: int = Config.MAX_WORDS) -> List[Word]:
        """從 Jisho.org 獲取 N1 詞彙"""
        words = []
        page = 1
        
        while len(words) < max_words and page <= Config.MAX_PAGES:
            new_words = self._fetch_page(page)
            if not new_words:
                break
            words.extend(new_words)
            page += 1
            
        return words[:max_words]
    
    def _fetch_page(self, page: int) -> List[Word]:
        """獲取單一頁面的詞彙"""
        url = f"https://jisho.org/search/%23jlpt-n1%20%23words?page={page}"
        try:
            response = requests.get(url, headers=self.headers, timeout=Config.JISHO_TIMEOUT)
            response.raise_for_status()
            return self._parse_page(response.text)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            return []
    
    def _parse_page(self, html: str) -> List[Word]:
        """解析頁面內容"""
        words = []
        soup = BeautifulSoup(html, 'lxml')
        
        for entry in soup.select('div.concept_light'):
            word = self._parse_entry(entry)
            if word:
                words.append(word)
                
        return words
    
    def _parse_entry(self, entry: BeautifulSoup) -> Optional[Word]:
        """解析單個詞條"""
        try:
            japanese = entry.select_one('.text').text.strip()
            if not any(ord(char) >= 0x3040 for char in japanese):
                return None
                
            hiragana = entry.select_one('.furigana').text.strip()
            meanings = []
            
            for meaning in entry.select('.meaning-meaning'):
                text = meaning.text.strip()
                if text and not text.startswith('('):
                    meanings.append(text)
                    
            if not meanings:
                return None
                
            meaning = '；'.join(meanings[:2])
            return Word.create(japanese, hiragana, meaning, -1)  # ID will be set by VocabularyService
            
        except Exception as e:
            print(f"Error parsing entry: {e}")
            return None 