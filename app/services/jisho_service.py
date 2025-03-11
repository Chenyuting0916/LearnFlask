import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from app.models.vocabulary import Word
from config.settings import Config
import random

class JishoService:
    """Jisho.org 網站爬蟲服務"""
    
    def __init__(self):
        self.headers = {'User-Agent': Config.JISHO_USER_AGENT}
    
    def fetch_n1_words(self, max_words: int = Config.MAX_WORDS) -> List[Word]:
        """從 Jisho.org 獲取 N1 詞彙"""
        all_words = []
        total_pages = self._get_total_pages()
        
        # 隨機選擇要抓取的頁面
        available_pages = list(range(1, total_pages + 1))
        random.shuffle(available_pages)
        target_pages = available_pages[:Config.MAX_PAGES]
        
        print(f"開始從 Jisho.org 抓取單字...")
        print(f"找到總共 {total_pages} 頁，將隨機抓取 {len(target_pages)} 頁")
        
        for page in target_pages:
            print(f"正在抓取第 {page} 頁...")
            new_words = self._fetch_page(page)
            if new_words:
                all_words.extend(new_words)
                print(f"目前已抓取 {len(all_words)} 個單字")
            
        # 如果抓到的單字超過需要的數量，隨機選擇所需數量的單字
        if len(all_words) > max_words:
            all_words = random.sample(all_words, max_words)
            
        print(f"抓取完成！共獲得 {len(all_words)} 個單字")
        return all_words
    
    def _get_total_pages(self) -> int:
        """獲取總頁數"""
        try:
            url = "https://jisho.org/search/%23jlpt-n1%20%23words"
            response = requests.get(url, headers=self.headers, timeout=Config.JISHO_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 找到最後一頁的連結
            last_page = soup.select('div.pagination a')[-2].text.strip()
            return int(last_page)
        except Exception as e:
            print(f"Error getting total pages: {e}")
            return Config.MAX_PAGES
    
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