from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 示例單字列表（實際應用中可以使用資料庫）
vocabulary = [
    {"japanese": "こんにちは", "hiragana": "こんにちは", "meaning": "你好"},
    {"japanese": "ありがとう", "hiragana": "ありがとう", "meaning": "謝謝"},
    {"japanese": "さようなら", "hiragana": "さようなら", "meaning": "再見"},
    {"japanese": "おはよう", "hiragana": "おはよう", "meaning": "早安"},
    {"japanese": "すみません", "hiragana": "すみません", "meaning": "對不起/打擾了"},
]

@app.route('/')
def home():
    return render_template('index.html', word=random.choice(vocabulary))

@app.route('/next')
def next_word():
    return jsonify(random.choice(vocabulary))

if __name__ == '__main__':
    app.run(debug=True) 