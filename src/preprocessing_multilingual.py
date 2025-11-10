"""
多語言文字前處理模組
支援中英文的垃圾郵件檢測
"""

import re
import string
import jieba  # 中文分詞
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# 下載必要的 NLTK 資源
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"⚠️  NLTK 資源下載失敗: {e}")


class MultilingualTextPreprocessor:
    """多語言文字前處理器（支援中英文）"""
    
    def __init__(self):
        # 英文停用詞
        try:
            self.en_stop_words = set(stopwords.words('english'))
        except:
            print("⚠️  無法載入英文停用詞，使用基本列表")
            self.en_stop_words = set(['i', 'me', 'my', 'we', 'you', 'he', 'she', 'it', 
                                      'they', 'the', 'a', 'an', 'and', 'or', 'but', 'is', 
                                      'are', 'was', 'were', 'to', 'of', 'in', 'on', 'at'])
        
        # 中文停用詞（常見的）
        self.zh_stop_words = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
            '一個', '上', '也', '很', '到', '說', '要', '去', '你', '會', '著', '沒有',
            '看', '好', '自己', '這', '那', '裡', '來', '們', '他', '她', '它', '這個',
            '那個', '什麼', '怎麼', '為什麼', '嗎', '吧', '啊', '呢', '呀'
        ])
        
        # 英文詞幹提取器
        try:
            self.stemmer = PorterStemmer()
        except:
            self.stemmer = None
    
    def detect_language(self, text):
        """
        檢測文字主要語言
        
        Returns:
            'zh': 中文為主
            'en': 英文為主
            'mixed': 混合
        """
        # 計算中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total = chinese_chars + english_chars
        
        if total == 0:
            return 'en'
        
        chinese_ratio = chinese_chars / total
        
        if chinese_ratio > 0.3:
            return 'zh'
        elif chinese_ratio > 0.1:
            return 'mixed'
        else:
            return 'en'
    
    def clean_text(self, text):
        """
        清理文字（保留中文）
        """
        if not isinstance(text, str):
            return ""
        
        # 轉小寫（只對英文）
        text = text.lower()
        
        # 移除 URL
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # 移除 email
        text = re.sub(r'\S+@\S+', '', text)
        
        # 移除標點符號（保留中文字符）
        # 只移除英文標點
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # 移除多餘空白
        text = ' '.join(text.split())
        
        return text
    
    def tokenize_chinese(self, text):
        """中文分詞"""
        words = jieba.cut(text)
        return ' '.join(words)
    
    def remove_stopwords(self, text, language='en'):
        """移除停用詞"""
        words = text.split()
        
        if language == 'zh' or language == 'mixed':
            # 中文停用詞
            filtered_words = [word for word in words 
                            if word not in self.zh_stop_words and len(word.strip()) > 0]
        else:
            # 英文停用詞
            filtered_words = [word for word in words 
                            if word not in self.en_stop_words and len(word.strip()) > 0]
        
        return ' '.join(filtered_words)
    
    def stem_text(self, text):
        """英文詞幹提取"""
        if not self.stemmer:
            return text
        words = text.split()
        # 只對純英文單詞進行詞幹提取
        stemmed_words = []
        for word in words:
            if re.match(r'^[a-z]+$', word):
                stemmed_words.append(self.stemmer.stem(word))
            else:
                stemmed_words.append(word)
        return ' '.join(stemmed_words)
    
    def preprocess(self, text):
        """完整的前處理流程（支援中英文）"""
        # 處理空值
        if not isinstance(text, str):
            return ""
        
        text = text.strip()
        if not text:
            return ""
        
        # 檢測語言
        language = self.detect_language(text)
        
        # 清理文字
        text = self.clean_text(text)
        
        if not text or not text.strip():
            return ""
        
        # 如果是中文，進行分詞
        if language in ['zh', 'mixed']:
            text = self.tokenize_chinese(text)
        
        # 移除停用詞
        text = self.remove_stopwords(text, language)
        
        if not text or not text.strip():
            return "text"
        
        # 只對英文進行詞幹提取
        if language == 'en':
            text = self.stem_text(text)
        
        return text if text and text.strip() else "text"


# 測試程式碼
if __name__ == "__main__":
    print("🧪 測試多語言文字前處理器...")
    
    preprocessor = MultilingualTextPreprocessor()
    
    test_cases = [
        ("恭喜！您中獎了！立即點擊領取獎金！", "中文垃圾郵件"),
        ("您好，明天下午3點開會，請準時參加。", "中文正常郵件"),
        ("WINNER!! You've won $1000! Call NOW!!!", "英文垃圾郵件"),
        ("Hi John, can we meet tomorrow at 3pm?", "英文正常郵件"),
        ("免費 Free! 立即獲取 Get it now!", "中英文混合"),
    ]
    
    for text, description in test_cases:
        language = preprocessor.detect_language(text)
        result = preprocessor.preprocess(text)
        print(f"\n{description} ({language}):")
        print(f"原始: {text}")
        print(f"處理: {result}")
    
    print("\n✅ 多語言前處理測試完成")
