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