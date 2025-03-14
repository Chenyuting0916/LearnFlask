class Hiragana:
    """平假名字符類"""
    def __init__(self, character, romaji, example_word=None, example_translation=None, audio_url=None):
        self.character = character  # 平假名字符
        self.romaji = romaji  # 羅馬字拼寫
        self.example_word = example_word  # 包含該字符的例詞
        self.example_translation = example_translation  # 例詞的翻譯
        self.audio_url = audio_url  # 發音音頻URL
        
class Katakana:
    """片假名字符類"""
    def __init__(self, character, romaji, example_word=None, example_translation=None, audio_url=None):
        self.character = character  # 片假名字符
        self.romaji = romaji  # 羅馬字拼寫
        self.example_word = example_word  # 包含該字符的例詞
        self.example_translation = example_translation  # 例詞的翻譯
        self.audio_url = audio_url  # 發音音頻URL

class Vocabulary:
    """日語詞彙類"""
    def __init__(self, id=None, word=None, reading=None, meaning=None, 
                 jlpt_level=None, example_sentence=None, example_translation=None, 
                 category=None, audio_url=None, is_premium=False):
        self.id = id
        self.word = word  # 日語單詞（漢字或假名）
        self.reading = reading  # 單詞的讀音（假名）
        self.meaning = meaning  # 意思（中文翻譯）
        self.jlpt_level = jlpt_level  # JLPT等級（N5-N1）
        self.example_sentence = example_sentence  # 示例句子
        self.example_translation = example_translation  # 示例句子的翻譯
        self.category = category  # 詞彙類別（如：動詞、名詞等）
        self.audio_url = audio_url  # 發音音頻URL
        self.is_premium = is_premium  # 是否僅限高級用戶使用
        
    def to_dict(self):
        """將詞彙對象轉換為字典"""
        return {
            'id': self.id,
            'word': self.word,
            'reading': self.reading,
            'meaning': self.meaning,
            'jlpt_level': self.jlpt_level,
            'example_sentence': self.example_sentence,
            'example_translation': self.example_translation,
            'category': self.category,
            'audio_url': self.audio_url,
            'is_premium': self.is_premium
        }
        
class Lesson:
    """日語課程類"""
    def __init__(self, id=None, title=None, description=None, level=None, 
                 content=None, vocabulary_ids=None, grammar_points=None, 
                 is_premium=False, price=0.0):
        self.id = id
        self.title = title  # 課程標題
        self.description = description  # 課程描述
        self.level = level  # 難度等級
        self.content = content  # 課程內容HTML或Markdown
        self.vocabulary_ids = vocabulary_ids or []  # 關聯詞彙的ID列表
        self.grammar_points = grammar_points or []  # 語法點列表
        self.is_premium = is_premium  # 是否為付費課程
        self.price = price  # 課程價格（如果是單獨銷售）
        
    def to_dict(self):
        """將課程對象轉換為字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'level': self.level,
            'content': self.content,
            'vocabulary_ids': self.vocabulary_ids,
            'grammar_points': self.grammar_points,
            'is_premium': self.is_premium,
            'price': self.price
        }

class Quiz:
    """測驗類"""
    def __init__(self, id=None, title=None, description=None, questions=None, level=None, is_premium=False):
        self.id = id
        self.title = title  # 測驗標題
        self.description = description  # 測驗描述
        self.questions = questions or []  # 問題列表
        self.level = level  # 難度等級
        self.is_premium = is_premium  # 是否僅限高級用戶使用
        
    def to_dict(self):
        """將測驗對象轉換為字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'questions': [q.to_dict() for q in self.questions],
            'level': self.level,
            'is_premium': self.is_premium
        }
        
class Question:
    """測驗問題類"""
    def __init__(self, id=None, text=None, options=None, correct_answer=None, explanation=None):
        self.id = id
        self.text = text  # 問題文本
        self.options = options or []  # 選項列表
        self.correct_answer = correct_answer  # 正確答案
        self.explanation = explanation  # 答案解釋
        
    def to_dict(self):
        """將問題對象轉換為字典"""
        return {
            'id': self.id,
            'text': self.text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation
        } 