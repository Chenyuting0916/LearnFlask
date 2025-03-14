class VocabularyApp {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }
    initializeElements() {
        const elements = {
            meaningButton: document.getElementById('showMeaning'),
            nextButton: document.getElementById('nextWord'),
            refreshButton: document.getElementById('refreshVocab'),
            meaningDiv: document.getElementById('meaning'),
            japaneseDiv: document.querySelector('.japanese'),
            hiraganaDiv: document.querySelector('.hiragana'),
            learnedWordsContainer: document.getElementById('learnedWords'),
            loadingDiv: document.getElementById('loading'),
            learnedCountSpan: document.getElementById('learnedCount'),
            totalCountSpan: document.getElementById('totalCount')
        };
        // Verify all elements exist
        Object.entries(elements).forEach(([key, element]) => {
            if (!element) {
                throw new Error(`Element ${key} not found`);
            }
        });
        // Type assertions after verification
        this.meaningButton = elements.meaningButton;
        this.nextButton = elements.nextButton;
        this.refreshButton = elements.refreshButton;
        this.meaningDiv = elements.meaningDiv;
        this.japaneseDiv = elements.japaneseDiv;
        this.hiraganaDiv = elements.hiraganaDiv;
        this.learnedWordsContainer = elements.learnedWordsContainer;
        this.loadingDiv = elements.loadingDiv;
        this.learnedCountSpan = elements.learnedCountSpan;
        this.totalCountSpan = elements.totalCountSpan;
    }
    setupEventListeners() {
        this.meaningButton.addEventListener('click', () => this.toggleMeaning());
        this.nextButton.addEventListener('click', () => this.loadNextWord());
        this.refreshButton.addEventListener('click', () => this.refreshVocabulary());
    }
    toggleMeaning() {
        if (this.meaningDiv.style.display === 'none' || !this.meaningDiv.style.display) {
            this.meaningDiv.style.display = 'block';
            this.meaningButton.textContent = '隱藏含義';
        }
        else {
            this.meaningDiv.style.display = 'none';
            this.meaningButton.textContent = '顯示含義';
        }
    }
    async loadNextWord() {
        try {
            const response = await fetch('/next');
            const data = await response.json();
            
            if (data.status === 'refreshed') {
                alert('已學習完所有單字！現在將載入新的單字。');
                this.learnedWordsContainer.innerHTML = '';  // 清空已學習單字列表
                this.learnedCountSpan.textContent = '0';
            }
            
            this.updateWord(data.word);
            this.updateLearnedWords(data.learned_words);
            this.learnedCountSpan.textContent = data.learned_words.length.toString();
        }
        catch (error) {
            console.error('Error loading next word:', error);
        }
    }
    async refreshVocabulary() {
        this.loadingDiv.style.display = 'block';
        this.refreshButton.disabled = true;
        try {
            const response = await fetch('/refresh-vocabulary');
            const data = await response.json();
            if (data.status === 'success' && data.count !== undefined) {
                this.totalCountSpan.textContent = data.count.toString();
                this.learnedWordsContainer.innerHTML = '';
                this.learnedCountSpan.textContent = '0';
                this.updateWord(data.word);
                this.updateLearnedWords(data.learned_words || []);
                alert(`成功更新單字庫！共載入 ${data.count} 個單字。`);
            }
        }
        catch (error) {
            alert('更新單字庫時發生錯誤，請稍後再試。');
            console.error('Error refreshing vocabulary:', error);
        }
        finally {
            this.loadingDiv.style.display = 'none';
            this.refreshButton.disabled = false;
        }
    }
    updateWord(word) {
        this.japaneseDiv.textContent = word.japanese;
        this.hiraganaDiv.textContent = word.hiragana;
        this.meaningDiv.textContent = word.meaning;
        this.meaningDiv.style.display = 'none';
        this.meaningButton.textContent = '顯示含義';
    }
    updateLearnedWords(words) {
        this.learnedWordsContainer.innerHTML = words
            .map(word => `
                <div class="learned-word">
                    <div class="japanese">${word.japanese}</div>
                    <div class="hiragana">${word.hiragana}</div>
                    <div class="meaning">${word.meaning}</div>
                </div>
            `)
            .join('');
    }
}
// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VocabularyApp();
});
export {};
//# sourceMappingURL=main.js.map

// 等待頁面完全加載
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 平假名和片假名學習頁面
    initializeKanaLearning();
    
    // 詞彙發音播放
    initializeAudioPlayback();
    
    // 測驗功能
    initializeQuiz();
    
    // 訂閱頁面功能
    initializeSubscription();
});

// 初始化假名學習功能
function initializeKanaLearning() {
    const kanaCards = document.querySelectorAll('.kana-card');
    
    kanaCards.forEach(card => {
        // 為每個假名卡片添加點擊效果
        card.addEventListener('click', function() {
            // 播放發音
            const audioElement = this.querySelector('audio');
            if (audioElement) {
                audioElement.play();
            }
            
            // 添加強調效果
            this.classList.add('highlight');
            setTimeout(() => {
                this.classList.remove('highlight');
            }, 500);
        });
    });
    
    // 假名練習遊戲（如果存在）
    const gameContainer = document.getElementById('kana-game');
    if (gameContainer) {
        initializeKanaGame();
    }
}

// 初始化假名練習遊戲
function initializeKanaGame() {
    const gameContainer = document.getElementById('kana-game');
    const optionButtons = gameContainer.querySelectorAll('.game-option');
    const nextButton = document.getElementById('next-question');
    const scoreDisplay = document.getElementById('score-display');
    
    let score = 0;
    let currentQuestion;
    
    // 下一個問題按鈕
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            generateQuestion();
            optionButtons.forEach(btn => {
                btn.classList.remove('correct', 'incorrect');
                btn.disabled = false;
            });
            this.disabled = true;
        });
    }
    
    // 選項按鈕
    optionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedAnswer = this.dataset.romaji;
            const correctAnswer = currentQuestion.romaji;
            
            optionButtons.forEach(btn => btn.disabled = true);
            
            if (selectedAnswer === correctAnswer) {
                this.classList.add('correct');
                score++;
                scoreDisplay.textContent = score;
            } else {
                this.classList.add('incorrect');
                // 顯示正確答案
                optionButtons.forEach(btn => {
                    if (btn.dataset.romaji === correctAnswer) {
                        btn.classList.add('correct');
                    }
                });
            }
            
            nextButton.disabled = false;
        });
    });
    
    // 生成問題
    function generateQuestion() {
        // 這裡假設我們有一個假名數據集
        // 實際應用中應該從服務器獲取或使用預定義數據
        const kanaData = window.kanaData || [
            { character: "あ", romaji: "a" },
            { character: "い", romaji: "i" },
            { character: "う", romaji: "u" },
            { character: "え", romaji: "e" },
            { character: "お", romaji: "o" }
        ];
        
        // 隨機選擇一個假名
        currentQuestion = kanaData[Math.floor(Math.random() * kanaData.length)];
        
        // 顯示問題
        const questionDisplay = document.getElementById('question-kana');
        if (questionDisplay) {
            questionDisplay.textContent = currentQuestion.character;
        }
        
        // 生成選項（包含正確答案和隨機錯誤答案）
        const options = [currentQuestion.romaji];
        while (options.length < 4) {
            const randomKana = kanaData[Math.floor(Math.random() * kanaData.length)];
            if (!options.includes(randomKana.romaji)) {
                options.push(randomKana.romaji);
            }
        }
        
        // 打亂選項順序
        shuffleArray(options);
        
        // 更新選項按鈕
        optionButtons.forEach((btn, index) => {
            if (index < options.length) {
                btn.textContent = options[index];
                btn.dataset.romaji = options[index];
            }
        });
    }
    
    // 如果遊戲容器存在，開始遊戲
    if (gameContainer && optionButtons.length > 0) {
        generateQuestion();
    }
}

// 初始化音頻播放功能
function initializeAudioPlayback() {
    const audioButtons = document.querySelectorAll('.play-audio');
    
    audioButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const audioUrl = this.dataset.audio;
            
            if (audioUrl) {
                const audio = new Audio(audioUrl);
                audio.play();
                
                // 添加播放圖標動畫
                this.classList.add('playing');
                setTimeout(() => {
                    this.classList.remove('playing');
                }, 1000);
            }
        });
    });
}

// 初始化測驗功能
function initializeQuiz() {
    const quizForm = document.getElementById('quiz-form');
    
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 模擬提交，實際應用中應向服務器發送數據
            const resultSection = document.getElementById('quiz-results');
            if (resultSection) {
                resultSection.classList.remove('d-none');
                scrollToElement(resultSection);
            }
        });
        
        // 為選項添加點擊事件
        const optionInputs = quizForm.querySelectorAll('input[type="radio"]');
        optionInputs.forEach(input => {
            input.addEventListener('change', function() {
                // 找到這個問題的所有選項
                const questionGroup = this.name;
                const groupInputs = quizForm.querySelectorAll(`input[name="${questionGroup}"]`);
                
                // 移除所有選中樣式
                groupInputs.forEach(groupInput => {
                    const label = document.querySelector(`label[for="${groupInput.id}"]`);
                    if (label) {
                        label.classList.remove('selected-option');
                    }
                });
                
                // 為當前選中的添加樣式
                const label = document.querySelector(`label[for="${this.id}"]`);
                if (label) {
                    label.classList.add('selected-option');
                }
            });
        });
    }
}

// 初始化訂閱功能
function initializeSubscription() {
    const planButtons = document.querySelectorAll('.select-plan');
    const monthSelect = document.getElementById('subscription-months');
    const priceDisplay = document.getElementById('price-display');
    const totalDisplay = document.getElementById('total-price');
    
    // 選擇訂閱計劃
    planButtons.forEach(button => {
        button.addEventListener('click', function() {
            const planType = this.dataset.plan;
            const planInput = document.getElementById('plan-type');
            
            if (planInput) {
                planInput.value = planType;
            }
            
            // 更新視覺樣式
            planButtons.forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected');
            
            // 更新價格
            updatePrice();
        });
    });
    
    // 選擇訂閱月數
    if (monthSelect) {
        monthSelect.addEventListener('change', function() {
            updatePrice();
        });
    }
    
    // 更新價格顯示
    function updatePrice() {
        if (!priceDisplay || !totalDisplay || !monthSelect) return;
        
        const selectedPlan = document.querySelector('.select-plan.selected');
        if (!selectedPlan) return;
        
        const basePrice = parseFloat(selectedPlan.dataset.price) || 0;
        const months = parseInt(monthSelect.value) || 1;
        const total = basePrice * months;
        
        // 顯示單價和總價
        priceDisplay.textContent = basePrice.toFixed(2);
        totalDisplay.textContent = total.toFixed(2);
    }
}

// 工具函數：滾動到指定元素
function scrollToElement(element) {
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// 工具函數：打亂數組
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}