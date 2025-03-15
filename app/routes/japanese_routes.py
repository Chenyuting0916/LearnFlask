from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.services import japanese_service
from app.models.japanese_content import Vocabulary, Lesson, Quiz
from app.services.vocabulary_service import VocabularyService
import random
import json
import os
import requests
from bs4 import BeautifulSoup
from app.services import auth_service

bp = Blueprint('japanese', __name__, url_prefix='/japanese')
vocabulary_service = VocabularyService()
current_word_index = 0

@bp.route('/')
def index():
    """日語學習主頁"""
    return render_template('japanese/index.html')

@bp.route('/hiragana')
def hiragana():
    """展示平假名學習頁面"""
    hiragana_chars = japanese_service.get_all_hiragana()
    
    # 創建統一格式的平假名數據
    hiragana_dict = {kana.romaji: kana for kana in hiragana_chars}
    
    # 如果發現資料不足，可以手動添加缺失的數據
    missing_hiragana = {
        'shi': {'character': 'し', 'example_word': 'しあわせ', 'example_translation': '幸福'},
        'chi': {'character': 'ち', 'example_word': 'ちから', 'example_translation': '力量'},
        'tsu': {'character': 'つ', 'example_word': 'つくえ', 'example_translation': '桌子'},
        'fu': {'character': 'ふ', 'example_word': 'ふゆ', 'example_translation': '冬天'},
        'ya': {'character': 'や', 'example_word': 'やま', 'example_translation': '山'},
        'yu': {'character': 'ゆ', 'example_word': 'ゆき', 'example_translation': '雪'},
        'yo': {'character': 'よ', 'example_word': 'よる', 'example_translation': '夜晚'}
    }
    
    # 將缺失的假名添加到字典中
    for romaji, data in missing_hiragana.items():
        if romaji not in hiragana_dict:
            from app.models.japanese_content import Hiragana
            hiragana_dict[romaji] = Hiragana(
                character=data['character'],
                romaji=romaji,
                example_word=data['example_word'],
                example_translation=data['example_translation']
            )
    
    # 將Hiragana對象轉換為可序列化的字典
    hiragana_list_serializable = []
    for kana in hiragana_dict.values():
        hiragana_list_serializable.append({
            'character': kana.character,
            'romaji': kana.romaji,
            'example_word': kana.example_word,
            'example_translation': kana.example_translation
        })
    
    return render_template(
        'japanese/hiragana.html', 
        hiragana_list=hiragana_list_serializable
    )

@bp.route('/katakana')
def katakana():
    """展示片假名學習頁面"""
    katakana_chars = japanese_service.get_all_katakana()
    
    # 創建統一格式的片假名數據
    katakana_dict = {kana.romaji: kana for kana in katakana_chars}
    
    # 如果發現資料不足，可以手動添加缺失的數據
    missing_katakana = {
        'shi': {'character': 'シ', 'example_word': 'シャツ', 'example_translation': '襯衫'},
        'chi': {'character': 'チ', 'example_word': 'チーズ', 'example_translation': '起司'},
        'tsu': {'character': 'ツ', 'example_word': 'ツアー', 'example_translation': '旅行團'},
        'fu': {'character': 'フ', 'example_word': 'フォーク', 'example_translation': '叉子'},
        'ya': {'character': 'ヤ', 'example_word': 'ヤクルト', 'example_translation': '養樂多'},
        'yu': {'character': 'ユ', 'example_word': 'ユーモア', 'example_translation': '幽默'},
        'yo': {'character': 'ヨ', 'example_word': 'ヨーロッパ', 'example_translation': '歐洲'}
    }
    
    # 將缺失的假名添加到字典中
    for romaji, data in missing_katakana.items():
        if romaji not in katakana_dict:
            from app.models.japanese_content import Katakana
            katakana_dict[romaji] = Katakana(
                character=data['character'],
                romaji=romaji,
                example_word=data['example_word'],
                example_translation=data['example_translation']
            )
    
    # 將Katakana對象轉換為可序列化的字典
    katakana_list_serializable = []
    for kana in katakana_dict.values():
        katakana_list_serializable.append({
            'character': kana.character,
            'romaji': kana.romaji,
            'example_word': kana.example_word,
            'example_translation': kana.example_translation
        })
    
    return render_template(
        'japanese/katakana.html', 
        katakana_list=katakana_list_serializable
    )

@bp.route('/vocabulary')
def vocabulary():
    """N1詞彙學習頁面"""
    return render_template('japanese/n1_vocabulary.html')

@bp.route('/vocabulary/<vocabulary_id>')
def vocabulary_detail(vocabulary_id):
    """詞彙詳情頁面"""
    vocabulary_items = japanese_service.get_vocabulary(vocabulary_id=vocabulary_id)
    if not vocabulary_items:
        flash('找不到該詞彙', 'error')
        return redirect(url_for('japanese.vocabulary'))
    
    return render_template('japanese/vocabulary_detail.html', vocabulary=vocabulary_items[0])

@bp.route('/lessons')
def lessons():
    """展示日語課程列表頁面"""
    flash('課程功能暫未開放', 'info')
    return redirect(url_for('japanese.index'))

@bp.route('/lessons/<lesson_id>')
def lesson_detail(lesson_id):
    """課程詳情頁面"""
    flash('課程功能暫未開放', 'info')
    return redirect(url_for('japanese.index'))

@bp.route('/quizzes')
def quizzes():
    """展示日語測驗列表頁面，僅限訂閱會員使用"""
    # 獲取過濾參數
    level = request.args.get('level', '')
    
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以使用測驗功能。', 'warning')
        return redirect(url_for('auth.login'))
    
    # 檢查用戶訂閱狀態
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    # 更新會話中的訂閱狀態
    session['user_subscription'] = user['subscription_type']
    
    # 檢查訂閱狀態
    if user['subscription_type'] == 'free':
        flash('測驗功能僅對訂閱會員開放，請升級訂閱以使用測驗功能。', 'warning')
        return redirect(url_for('auth.subscription'))
    
    # 從服務層獲取測驗列表
    quizzes = japanese_service.get_quizzes(level=level if level else None)
    
    # 獲取用戶測驗歷史記錄
    user_quiz_history = japanese_service.get_user_quiz_history(session['user_id'])
    
    return render_template('japanese/quizzes.html', 
                          quizzes=quizzes,
                          user_quiz_history=user_quiz_history,
                          user_subscription=user['subscription_type'])

@bp.route('/quizzes/<quiz_id>')
def quiz_detail(quiz_id):
    """測驗詳情頁面，僅限訂閱會員使用"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以使用測驗功能。', 'warning')
        return redirect(url_for('auth.login'))
    
    # 檢查用戶訂閱狀態
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    # 更新會話中的訂閱狀態
    session['user_subscription'] = user['subscription_type']
    
    # 檢查訂閱狀態
    if user['subscription_type'] == 'free':
        flash('測驗功能僅對訂閱會員開放，請升級訂閱以使用測驗功能。', 'warning')
        return redirect(url_for('auth.subscription'))
        
    quiz_items = japanese_service.get_quizzes(quiz_id=quiz_id)
    if not quiz_items:
        flash('找不到該測驗', 'error')
        return redirect(url_for('japanese.quizzes'))
    
    quiz = quiz_items[0]
    
    return render_template('japanese/quiz_detail.html', quiz=quiz)

@bp.route('/quizzes/<quiz_id>/submit', methods=['POST'])
def quiz_submit(quiz_id):
    """測驗提交，僅限訂閱會員使用"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以使用測驗功能。', 'warning')
        return redirect(url_for('auth.login'))
    
    # 檢查用戶訂閱狀態
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    # 更新會話中的訂閱狀態
    session['user_subscription'] = user['subscription_type']
    
    # 檢查訂閱狀態
    if user['subscription_type'] == 'free':
        flash('測驗功能僅對訂閱會員開放，請升級訂閱以使用測驗功能。', 'warning')
        return redirect(url_for('auth.subscription'))
        
    quiz_items = japanese_service.get_quizzes(quiz_id=quiz_id)
    if not quiz_items:
        flash('找不到該測驗', 'error')
        return redirect(url_for('japanese.quizzes'))
    
    quiz = quiz_items[0]
    
    # 獲取用戶答案
    user_answers = {}
    for question in quiz.questions:
        user_answers[question.id] = request.form.get(f'question_{question.id}')
    
    # 計算分數
    correct_count = 0
    results = {}
    for question in quiz.questions:
        is_correct = user_answers.get(question.id) == question.correct_answer
        if is_correct:
            correct_count += 1
        results[question.id] = {
            'user_answer': user_answers.get(question.id),
            'correct_answer': question.correct_answer,
            'is_correct': is_correct,
            'explanation': question.explanation
        }
    
    score = int((correct_count / len(quiz.questions)) * 100)
    
    # 記錄測驗歷史
    japanese_service.add_quiz_history(
        user_id=session['user_id'],
        quiz_id=quiz_id,
        score=score,
        answers=user_answers
    )
    
    return render_template('japanese/quiz_result.html', 
                          quiz=quiz, 
                          results=results, 
                          score=score)

@bp.route('/n1_vocabulary')
def n1_vocabulary():
    """N1詞彙學習頁面"""
    return render_template('japanese/n1_vocabulary.html')

@bp.route('/api/n1_vocabulary')
def api_n1_vocabulary():
    """API端點，用於獲取N1詞彙"""
    try:
        # 獲取請求參數
        count = request.args.get('count', default=10, type=int)
        count = min(max(count, 1), 50)  # 限制一次最多返回50個詞彙
        
        # 從Jisho.org獲取詞彙
        vocabulary_list = []
        
        # 隨機選擇一個起始頁碼
        start_page = random.randint(1, 15)  # Jisho有多個頁面的N1詞彙
        
        # 獲取多個頁面的詞彙
        current_count = 0
        current_page = start_page
        max_pages = 5  # 最多搜索5個頁面
        
        while current_count < count and max_pages > 0:
            # 從Jisho.org獲取詞彙
            url = f"https://jisho.org/search/%23jlpt-n1?page={current_page}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print(f"正在爬取Jisho頁面: {url}")
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return jsonify({'error': f"無法從Jisho獲取詞彙，狀態碼: {response.status_code}"}), 500
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 獲取詞彙列表
            vocabulary_items = soup.select('#primary .concept_light')
            print(f"找到 {len(vocabulary_items)} 個詞彙項目")
            
            if not vocabulary_items:
                max_pages -= 1
                current_page += 1
                continue
            
            # 隨機排序詞彙項
            random.shuffle(vocabulary_items)
            
            # 提取詞彙信息
            for item in vocabulary_items:
                if current_count >= count:
                    break
                
                word = item.select_one('.text').text.strip() if item.select_one('.text') else "N/A"
                reading = item.select_one('.furigana').text.strip() if item.select_one('.furigana') else ""
                
                # 調試信息
                print(f"\n處理詞彙: {word}, 讀音: {reading}")
                
                # 獲取英文意思 - 完全重寫這部分
                meanings = []
                
                # 方法1: 直接獲取英文意思部分
                english_senses = item.select('.meaning-wrapper')
                for sense in english_senses:
                    meaning_text = sense.select_one('.meaning-meaning')
                    if meaning_text:
                        clean_text = meaning_text.text.strip()
                        if clean_text:
                            meanings.append(clean_text)
                            print(f"方法1找到意思: {clean_text}")
                
                # 方法2: 如果方法1未找到，嘗試另一個選擇器
                if not meanings:
                    definition_items = item.select('.entries .entry .definition-item')
                    for def_item in definition_items:
                        clean_text = def_item.text.strip()
                        if clean_text:
                            meanings.append(clean_text)
                            print(f"方法2找到意思: {clean_text}")
                
                # 方法3: 最後嘗試查找所有包含英文釋義的元素
                if not meanings:
                    all_texts = item.select('.meanings_wrapper')
                    for text_item in all_texts:
                        clean_text = text_item.text.strip().replace('\n', ' ').replace('  ', ' ')
                        if clean_text:
                            # 如果文本太長，剪裁它
                            if len(clean_text) > 200:
                                clean_text = clean_text[:197] + "..."
                            meanings.append(clean_text)
                            print(f"方法3找到意思: {clean_text}")
                
                # 使用第一個有效意思，否則提供默認消息
                meaning = next((m for m in meanings if m), "No English definition found")
                print(f"最終使用的意思: {meaning}")
                
                # 構建詞彙項
                vocabulary = {
                    'id': str(current_count + 1),
                    'word': word,
                    'reading': reading,
                    'meaning': meaning,  # 英文釋義
                    'example_sentence': None,
                    'example_translation': None
                }
                
                vocabulary_list.append(vocabulary)
                current_count += 1
            
            max_pages -= 1
            current_page += 1
        
        # 日誌輸出所有找到的詞彙
        print(f"\n總共找到 {len(vocabulary_list)} 個詞彙")
        for i, vocab in enumerate(vocabulary_list):
            print(f"{i+1}. {vocab['word']} ({vocab['reading']}): {vocab['meaning']}")
        
        # 估計總詞彙數
        total_words = 1000  # 估計N1級別約有1000個詞彙
        
        return jsonify({
            'vocabulary_list': vocabulary_list,
            'current_page': start_page,
            'total_pages': 20,
            'total_words': total_words,
            'count': len(vocabulary_list)
        })
    except Exception as e:
        print(f"獲取詞彙時出錯: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"獲取詞彙時出錯: {str(e)}"}), 500 

@bp.route('/jlpt-quiz')
@bp.route('/jlpt-quiz/<level>/<year>/<section>')
def jlpt_quiz(level=None, year=None, section=None):
    """JLPT 真題測驗"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以參加測驗', 'warning')
        return redirect(url_for('auth.login'))
    
    # 檢查用戶是否為付費會員
    user_subscription = session.get('user_subscription', 'free')
    if user_subscription == 'free':
        flash('JLPT 測驗為付費功能，請升級會員以繼續', 'warning')
        return redirect(url_for('auth.subscription'))
    
    # 獲取所有可用的測驗
    quizzes = japanese_service.get_jlpt_quizzes()
    
    # 如果沒有指定具體測驗，顯示測驗列表
    if not all([level, year, section]):
        return render_template('japanese/jlpt_quiz.html', quizzes=quizzes)
    
    # 獲取指定的測驗
    quiz = japanese_service.get_jlpt_quiz(level, year, section)
    
    return render_template('japanese/jlpt_quiz.html',
                         quizzes=quizzes,
                         quiz=quiz,
                         level=level,
                         year=year,
                         section=section)

@bp.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    """提交 JLPT 測驗答案"""
    if 'user_id' not in session:
        flash('請先登錄以提交答案', 'warning')
        return redirect(url_for('auth.login'))
    
    # 檢查用戶是否為付費會員
    user_subscription = session.get('user_subscription', 'free')
    if user_subscription == 'free':
        flash('JLPT 測驗為付費功能，請升級會員以繼續', 'warning')
        return redirect(url_for('auth.subscription'))
    
    # 獲取測驗信息
    level = request.form.get('level')
    year = request.form.get('year')
    section = request.form.get('section')
    
    # 獲取答案
    answers = {}
    for key, value in request.form.items():
        if key.startswith('answer_'):
            question_id = int(key.split('_')[1])
            answers[question_id] = int(value)
    
    # 獲取測驗題目和正確答案
    quiz = japanese_service.get_jlpt_quiz(level, year, section)
    
    # 計算得分和生成解析
    total_questions = len(quiz['questions'])
    correct_answers = 0
    results = []
    
    for question in quiz['questions']:
        user_answer = answers.get(question['id'])
        is_correct = user_answer == question['correct_answer']
        if is_correct:
            correct_answers += 1
        
        results.append({
            'question': question['question'],
            'user_answer': question['options'][user_answer] if user_answer is not None else None,
            'correct_answer': question['options'][question['correct_answer']],
            'is_correct': is_correct,
            'explanation': question['explanation']
        })
    
    score = (correct_answers / total_questions) * 100
    
    # 保存測驗結果
    japanese_service.save_quiz_result(
        user_id=session['user_id'],
        quiz_type='JLPT',
        level=level,
        year=year,
        section=section,
        score=score,
        answers=answers
    )
    
    return render_template('japanese/quiz_result.html',
                         level=level,
                         year=year,
                         section=section,
                         score=score,
                         results=results) 