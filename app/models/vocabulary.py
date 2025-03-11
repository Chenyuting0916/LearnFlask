from dataclasses import dataclass
from typing import List

@dataclass
class Word:
    """日語單詞數據模型"""
    japanese: str    # 日語單詞（漢字）
    hiragana: str    # 平假名讀音
    meaning: str     # 中文含義
    id: int         # 單詞ID

    @classmethod
    def create(cls, japanese: str, hiragana: str, meaning: str, id: int) -> 'Word':
        """創建 Word 實例的工廠方法"""
        return cls(
            japanese=japanese,
            hiragana=hiragana or japanese,
            meaning=meaning,
            id=id
        ) 