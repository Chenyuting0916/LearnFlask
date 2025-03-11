import random
from flask import Blueprint, render_template, jsonify, session
from app.services.vocabulary_service import VocabularyService

bp = Blueprint('vocabulary', __name__)
vocabulary_service = VocabularyService()
current_word_index = 0

@bp.route('/')
def home():
    """首頁路由"""
    global current_word_index
    word = vocabulary_service.get_word(current_word_index)
    learned_words = vocabulary_service.get_learned_words()
    
    return render_template('index.html',
                         word=word,
                         learned_words=learned_words,
                         vocabulary=vocabulary_service.vocabulary)

@bp.route('/next')
def next_word():
    """下一個單字路由"""
    global current_word_index
    
    # 將當前單字加入已學習列表
    vocabulary_service.add_learned_word(current_word_index)

    # 獲取未學習的單字索引
    remaining_words = [i for i in range(len(vocabulary_service.vocabulary))
                      if i not in vocabulary_service.learned_words]
    
    if not remaining_words:
        vocabulary_service.refresh()
        current_word_index = 0
        word = vocabulary_service.get_word(0)
        return jsonify({
            "status": "refreshed",
            "word": word,
            "learned_words": vocabulary_service.get_learned_words()  # 返回空的已學習單字列表
        })
    
    current_word_index = random.choice(remaining_words)
    return jsonify({
        "status": "success",
        "word": vocabulary_service.get_word(current_word_index),
        "learned_words": vocabulary_service.get_learned_words()
    })

@bp.route('/refresh-vocabulary')
def refresh_vocabulary():
    """重新加載詞彙路由"""
    global current_word_index
    count = vocabulary_service.refresh()
    # 隨機選擇一個單字作為開始
    current_word_index = random.randint(0, count - 1) if count > 0 else 0
    word = vocabulary_service.get_word(current_word_index)
    return jsonify({
        "status": "success", 
        "count": count,
        "word": word,
        "learned_words": []
    }) 