import json
import os
from app.models.japanese_content import Hiragana, Katakana, Vocabulary, Lesson, Quiz, Question

# 數據文件路徑
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
HIRAGANA_FILE = os.path.join(DATA_DIR, 'hiragana.json')
KATAKANA_FILE = os.path.join(DATA_DIR, 'katakana.json')
VOCABULARY_FILE = os.path.join(DATA_DIR, 'vocabulary.json')
LESSON_FILE = os.path.join(DATA_DIR, 'lessons.json')
QUIZ_FILE = os.path.join(DATA_DIR, 'quizzes.json')

def _ensure_data_dir():
    """確保數據目錄存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _initialize_data_files():
    """初始化所有數據文件（如不存在）"""
    _ensure_data_dir()
    
    # 強制重新初始化平假名文件
    hiragana_data = [
        {"character": "あ", "romaji": "a", "example_word": "あめ", "example_translation": "雨"},
        {"character": "い", "romaji": "i", "example_word": "いぬ", "example_translation": "狗"},
        {"character": "う", "romaji": "u", "example_word": "うみ", "example_translation": "海"},
        {"character": "え", "romaji": "e", "example_word": "えき", "example_translation": "車站"},
        {"character": "お", "romaji": "o", "example_word": "おと", "example_translation": "聲音"},
        {"character": "か", "romaji": "ka", "example_word": "かみ", "example_translation": "紙"},
        {"character": "き", "romaji": "ki", "example_word": "きた", "example_translation": "北"},
        {"character": "く", "romaji": "ku", "example_word": "くに", "example_translation": "國家"},
        {"character": "け", "romaji": "ke", "example_word": "けん", "example_translation": "縣"},
        {"character": "こ", "romaji": "ko", "example_word": "こと", "example_translation": "事"},
        {"character": "さ", "romaji": "sa", "example_word": "さく", "example_translation": "咲"},
        {"character": "し", "romaji": "shi", "example_word": "しま", "example_translation": "島"},
        {"character": "す", "romaji": "su", "example_word": "すし", "example_translation": "壽司"},
        {"character": "せ", "romaji": "se", "example_word": "せん", "example_translation": "線"},
        {"character": "そ", "romaji": "so", "example_word": "そら", "example_translation": "天空"},
        {"character": "た", "romaji": "ta", "example_word": "たべる", "example_translation": "吃"},
        {"character": "ち", "romaji": "chi", "example_word": "ちず", "example_translation": "地圖"},
        {"character": "つ", "romaji": "tsu", "example_word": "つき", "example_translation": "月亮"},
        {"character": "て", "romaji": "te", "example_word": "てがみ", "example_translation": "信"},
        {"character": "と", "romaji": "to", "example_word": "とり", "example_translation": "鳥"},
        {"character": "な", "romaji": "na", "example_word": "なつ", "example_translation": "夏天"},
        {"character": "に", "romaji": "ni", "example_word": "にわ", "example_translation": "花園"},
        {"character": "ぬ", "romaji": "nu", "example_word": "ぬの", "example_translation": "布"},
        {"character": "ね", "romaji": "ne", "example_word": "ねこ", "example_translation": "貓"},
        {"character": "の", "romaji": "no", "example_word": "のみもの", "example_translation": "飲料"},
        {"character": "は", "romaji": "ha", "example_word": "はな", "example_translation": "花"},
        {"character": "ひ", "romaji": "hi", "example_word": "ひる", "example_translation": "中午"},
        {"character": "ふ", "romaji": "fu", "example_word": "ふゆ", "example_translation": "冬天"},
        {"character": "へ", "romaji": "he", "example_word": "へや", "example_translation": "房間"},
        {"character": "ほ", "romaji": "ho", "example_word": "ほん", "example_translation": "書"}
    ]
    with open(HIRAGANA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hiragana_data, f, ensure_ascii=False, indent=2)
    
    # 強制重新初始化片假名文件
    katakana_data = [
        {"character": "ア", "romaji": "a", "example_word": "アメリカ", "example_translation": "美國", "audio_url": ""},
        {"character": "イ", "romaji": "i", "example_word": "イギリス", "example_translation": "英國", "audio_url": ""},
        {"character": "ウ", "romaji": "u", "example_word": "ウール", "example_translation": "羊毛", "audio_url": ""},
        {"character": "エ", "romaji": "e", "example_word": "エレベーター", "example_translation": "電梯", "audio_url": ""},
        {"character": "オ", "romaji": "o", "example_word": "オーストラリア", "example_translation": "澳大利亞", "audio_url": ""},
        {"character": "カ", "romaji": "ka", "example_word": "カメラ", "example_translation": "相機", "audio_url": ""},
        {"character": "キ", "romaji": "ki", "example_word": "キーボード", "example_translation": "鍵盤", "audio_url": ""},
        {"character": "ク", "romaji": "ku", "example_word": "クラス", "example_translation": "班級", "audio_url": ""},
        {"character": "ケ", "romaji": "ke", "example_word": "ケーキ", "example_translation": "蛋糕", "audio_url": ""},
        {"character": "コ", "romaji": "ko", "example_word": "コーヒー", "example_translation": "咖啡", "audio_url": ""},
        {"character": "サ", "romaji": "sa", "example_word": "サイト", "example_translation": "網站", "audio_url": ""},
        {"character": "シ", "romaji": "shi", "example_word": "シャツ", "example_translation": "襯衫", "audio_url": ""},
        {"character": "ス", "romaji": "su", "example_word": "スポーツ", "example_translation": "運動", "audio_url": ""},
        {"character": "セ", "romaji": "se", "example_word": "セーター", "example_translation": "毛衣", "audio_url": ""},
        {"character": "ソ", "romaji": "so", "example_word": "ソファ", "example_translation": "沙發", "audio_url": ""},
        {"character": "タ", "romaji": "ta", "example_word": "タクシー", "example_translation": "計程車", "audio_url": ""},
        {"character": "チ", "romaji": "chi", "example_word": "チョコレート", "example_translation": "巧克力", "audio_url": ""},
        {"character": "ツ", "romaji": "tsu", "example_word": "ツアー", "example_translation": "旅行團", "audio_url": ""},
        {"character": "テ", "romaji": "te", "example_word": "テスト", "example_translation": "測試", "audio_url": ""},
        {"character": "ト", "romaji": "to", "example_word": "トマト", "example_translation": "番茄", "audio_url": ""},
        {"character": "ナ", "romaji": "na", "example_word": "ナイフ", "example_translation": "刀", "audio_url": ""},
        {"character": "ニ", "romaji": "ni", "example_word": "ニュース", "example_translation": "新聞", "audio_url": ""},
        {"character": "ヌ", "romaji": "nu", "example_word": "ヌガー", "example_translation": "牛軋糖", "audio_url": ""},
        {"character": "ネ", "romaji": "ne", "example_word": "ネクタイ", "example_translation": "領帶", "audio_url": ""},
        {"character": "ノ", "romaji": "no", "example_word": "ノート", "example_translation": "筆記本", "audio_url": ""},
        {"character": "ハ", "romaji": "ha", "example_word": "ハンバーガー", "example_translation": "漢堡", "audio_url": ""},
        {"character": "ヒ", "romaji": "hi", "example_word": "ヒーター", "example_translation": "暖氣", "audio_url": ""},
        {"character": "フ", "romaji": "fu", "example_word": "フランス", "example_translation": "法國", "audio_url": ""},
        {"character": "ヘ", "romaji": "he", "example_word": "ヘルメット", "example_translation": "頭盔", "audio_url": ""},
        {"character": "ホ", "romaji": "ho", "example_word": "ホテル", "example_translation": "旅館", "audio_url": ""},
        {"character": "マ", "romaji": "ma", "example_word": "マンゴー", "example_translation": "芒果", "audio_url": ""},
        {"character": "ミ", "romaji": "mi", "example_word": "ミルク", "example_translation": "牛奶", "audio_url": ""},
        {"character": "ム", "romaji": "mu", "example_word": "ムース", "example_translation": "慕斯", "audio_url": ""},
        {"character": "メ", "romaji": "me", "example_word": "メニュー", "example_translation": "菜單", "audio_url": ""},
        {"character": "モ", "romaji": "mo", "example_word": "モデル", "example_translation": "模特", "audio_url": ""},
        {"character": "ヤ", "romaji": "ya", "example_word": "ヤクルト", "example_translation": "優酪乳", "audio_url": ""},
        {"character": "ユ", "romaji": "yu", "example_word": "ユニフォーム", "example_translation": "制服", "audio_url": ""},
        {"character": "ヨ", "romaji": "yo", "example_word": "ヨガ", "example_translation": "瑜伽", "audio_url": ""},
        {"character": "ラ", "romaji": "ra", "example_word": "ラジオ", "example_translation": "收音機", "audio_url": ""},
        {"character": "リ", "romaji": "ri", "example_word": "リンゴ", "example_translation": "蘋果", "audio_url": ""},
        {"character": "ル", "romaji": "ru", "example_word": "ルール", "example_translation": "規則", "audio_url": ""},
        {"character": "レ", "romaji": "re", "example_word": "レストラン", "example_translation": "餐廳", "audio_url": ""},
        {"character": "ロ", "romaji": "ro", "example_word": "ロボット", "example_translation": "機器人", "audio_url": ""},
        {"character": "ワ", "romaji": "wa", "example_word": "ワイン", "example_translation": "葡萄酒", "audio_url": ""},
        {"character": "ヲ", "romaji": "wo", "example_word": "ヲタク", "example_translation": "御宅族", "audio_url": ""},
        {"character": "ン", "romaji": "n", "example_word": "アンケート", "example_translation": "問卷調查", "audio_url": ""}
    ]
    with open(KATAKANA_FILE, 'w', encoding='utf-8') as f:
        json.dump(katakana_data, f, ensure_ascii=False, indent=2)
    
    # 初始化詞彙文件
    if not os.path.exists(VOCABULARY_FILE):
        vocabulary_data = [
            {
                "id": "1",
                "word": "こんにちは",
                "reading": "こんにちは",
                "meaning": "你好",
                "jlpt_level": "N5",
                "example_sentence": "こんにちは、元気ですか？",
                "example_translation": "你好，你好嗎？",
                "category": "問候語",
                "audio_url": "/static/audio/vocabulary/konnichiwa.mp3",
                "is_premium": False
            },
            {
                "id": "2",
                "word": "ありがとう",
                "reading": "ありがとう",
                "meaning": "謝謝",
                "jlpt_level": "N5",
                "example_sentence": "ありがとう、助かります。",
                "example_translation": "謝謝，真是幫了大忙。",
                "category": "問候語",
                "audio_url": "/static/audio/vocabulary/arigatou.mp3",
                "is_premium": False
            }
        ]
        with open(VOCABULARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(vocabulary_data, f, ensure_ascii=False, indent=2)
    
    # 初始化課程文件
    if not os.path.exists(LESSON_FILE):
        lesson_data = [
            {
                "id": "1",
                "title": "日語入門：平假名",
                "description": "學習日語基礎：平假名的寫法和發音。",
                "level": "初級",
                "content": "<h1>平假名入門</h1><p>平假名是日語的基本假名系統之一，用於表示日語中的所有發音。</p><p>讓我們從五個基本元音開始：あ (a)、い (i)、う (u)、え (e)、お (o)</p>",
                "vocabulary_ids": ["1", "2"],
                "grammar_points": ["日語的元音發音", "平假名的筆順"],
                "is_premium": False,
                "price": 0.0
            },
            {
                "id": "2",
                "title": "日語入門：片假名",
                "description": "學習日語基礎：片假名的寫法和發音。",
                "level": "初級",
                "content": "<h1>片假名入門</h1><p>片假名主要用於表示外來語和外國名稱。</p><p>讓我們從五個基本元音開始：ア (a)、イ (i)、ウ (u)、エ (e)、オ (o)</p>",
                "vocabulary_ids": [],
                "grammar_points": ["片假名的用法", "片假名的筆順"],
                "is_premium": True,
                "price": 5.99
            }
        ]
        with open(LESSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(lesson_data, f, ensure_ascii=False, indent=2)
    
    # 初始化測驗文件
    if not os.path.exists(QUIZ_FILE):
        quiz_data = [
            {
                "id": "1",
                "title": "平假名測驗",
                "description": "測試你的平假名知識",
                "level": "初級",
                "is_premium": False,
                "questions": [
                    {
                        "id": "q1",
                        "text": "「あ」的正確發音是什麼？",
                        "options": ["a", "i", "u", "e"],
                        "correct_answer": "a",
                        "explanation": "「あ」的發音是「a」，如「apple」中的「a」。"
                    },
                    {
                        "id": "q2",
                        "text": "「い」的正確發音是什麼？",
                        "options": ["a", "i", "u", "e"],
                        "correct_answer": "i",
                        "explanation": "「い」的發音是「i」，如「meet」中的「ee」。"
                    }
                ]
            }
        ]
        with open(QUIZ_FILE, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)

# 初始化數據
_initialize_data_files()

# 平假名相關方法
def get_all_hiragana():
    """獲取所有平假名字符"""
    with open(HIRAGANA_FILE, 'r', encoding='utf-8') as f:
        hiragana_data = json.load(f)
    return [Hiragana(**data) for data in hiragana_data]

# 片假名相關方法
def get_all_katakana():
    """獲取所有片假名字符"""
    with open(KATAKANA_FILE, 'r', encoding='utf-8') as f:
        katakana_data = json.load(f)
    return [Katakana(**data) for data in katakana_data]

# 詞彙相關方法
def get_vocabulary(vocabulary_id=None, jlpt_level=None, is_premium=None):
    """獲取詞彙列表，可按ID、JLPT等級或高級狀態過濾"""
    with open(VOCABULARY_FILE, 'r', encoding='utf-8') as f:
        vocabulary_data = json.load(f)
    
    result = []
    for data in vocabulary_data:
        # 過濾條件
        if vocabulary_id and data['id'] != vocabulary_id:
            continue
        if jlpt_level and data['jlpt_level'] != jlpt_level:
            continue
        if is_premium is not None and data['is_premium'] != is_premium:
            continue
        
        result.append(Vocabulary(**data))
    
    return result

def add_vocabulary(vocabulary):
    """添加新詞彙"""
    with open(VOCABULARY_FILE, 'r', encoding='utf-8') as f:
        vocabulary_data = json.load(f)
    
    # 確保ID不重複
    existing_ids = [v['id'] for v in vocabulary_data]
    if vocabulary.id in existing_ids:
        return False, "詞彙ID已存在"
    
    vocabulary_data.append(vocabulary.to_dict())
    
    with open(VOCABULARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocabulary_data, f, ensure_ascii=False, indent=2)
    
    return True, None

# 課程相關方法
def get_lessons(lesson_id=None, level=None, is_premium=None):
    """獲取課程列表，可按ID、等級或高級狀態過濾"""
    with open(LESSON_FILE, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    result = []
    for data in lesson_data:
        # 過濾條件
        if lesson_id and data['id'] != lesson_id:
            continue
        if level and data['level'] != level:
            continue
        if is_premium is not None and data['is_premium'] != is_premium:
            continue
        
        result.append(Lesson(**data))
    
    return result

def add_lesson(lesson):
    """添加新課程"""
    with open(LESSON_FILE, 'r', encoding='utf-8') as f:
        lesson_data = json.load(f)
    
    # 確保ID不重複
    existing_ids = [l['id'] for l in lesson_data]
    if lesson.id in existing_ids:
        return False, "課程ID已存在"
    
    lesson_data.append(lesson.to_dict())
    
    with open(LESSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(lesson_data, f, ensure_ascii=False, indent=2)
    
    return True, None

# 測驗相關方法
def get_quizzes(quiz_id=None, level=None, is_premium=None):
    """獲取測驗列表，可按ID、等級或高級狀態過濾"""
    with open(QUIZ_FILE, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    result = []
    for data in quiz_data:
        # 過濾條件
        if quiz_id and data['id'] != quiz_id:
            continue
        if level and data['level'] != level:
            continue
        if is_premium is not None and data['is_premium'] != is_premium:
            continue
        
        # 處理問題對象
        questions = []
        for q_data in data.get('questions', []):
            questions.append(Question(**q_data))
        
        # 創建測驗對象
        quiz_obj = Quiz(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            level=data['level'],
            is_premium=data['is_premium'],
            questions=questions
        )
        
        result.append(quiz_obj)
    
    return result 