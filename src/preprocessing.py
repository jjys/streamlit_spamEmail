"""
資料前處理模組
負責清理和準備文字資料
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# 下載必要的 NLTK 資源
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"⚠️  NLTK 資源下載失敗: {e}")


class TextPreprocessor:
    """文字前處理器"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            print("⚠️  無法載入停用詞，將使用基本停用詞列表")
            # 使用基本的英文停用詞
            self.stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
                                  'ourselves', 'you', 'your', 'yours', 'yourself', 
                                  'yourselves', 'he', 'him', 'his', 'himself', 'she',
                                  'her', 'hers', 'herself', 'it', 'its', 'itself',
                                  'they', 'them', 'their', 'theirs', 'themselves',
                                  'what', 'which', 'who', 'whom', 'this', 'that',
                                  'these', 'those', 'am', 'is', 'are', 'was', 'were',
                                  'be', 'been', 'being', 'have', 'has', 'had', 'having',
                                  'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
                                  'but', 'if', 'or', 'because', 'as', 'until', 'while',
                                  'of', 'at', 'by', 'for', 'with', 'about', 'against',
                                  'between', 'into', 'through', 'during', 'before',
                                  'after', 'above', 'below', 'to', 'from', 'up', 'down',
                                  'in', 'out', 'on', 'off', 'over', 'under', 'again',
                                  'further', 'then', 'once'])
        
        try:
            self.stemmer = PorterStemmer()
        except:
            print("⚠️  無法載入詞幹提取器")
            self.stemmer = None
    
    def clean_text(self, text):
        """
        清理文字
        
        Args:
            text (str): 原始文字
            
        Returns:
            str: 清理後的文字
        """
        # 處理空值
        if not isinstance(text, str):
            return ""
        
        # 轉小寫
        text = text.lower()
        
        # 移除標點符號
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # 移除數字
        text = re.sub(r'\d+', '', text)
        
        # 移除多餘空白
        text = ' '.join(text.split())
        
        return text
    
    def remove_stopwords(self, text):
        """移除停用詞"""
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def stem_text(self, text):
        """詞幹提取"""
        if not self.stemmer:
            return text
        words = text.split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    def preprocess(self, text):
        """完整的前處理流程"""
        # 處理空值或非字串
        if not isinstance(text, str):
            return ""
        
        text = text.strip()
        if not text:
            return ""
        
        text = self.clean_text(text)
        
        # 如果清理後文字為空，直接返回
        if not text or not text.strip():
            return ""
        
        text = self.remove_stopwords(text)
        
        # 如果移除停用詞後為空，返回清理後的文字
        if not text or not text.strip():
            text = self.clean_text(text.strip() if isinstance(text, str) else "")
            return text if text else "text"  # 至少返回一個字
        
        text = self.stem_text(text)
        
        # 確保最終結果不為空
        return text if text and text.strip() else "text"


# 測試程式碼
if __name__ == "__main__":
    print("🧪 測試文字前處理器...")
    
    preprocessor = TextPreprocessor()
    
    test_cases = [
        "WINNER!! You've won $1000! Call NOW!!!",
        "Hi John, can we meet tomorrow at 3pm?",
        "Free delivery on your next order today!"
    ]
    
    for text in test_cases:
        result = preprocessor.preprocess(text)
        print(f"\n原始: {text}")
        print(f"處理: {result}")
    
    print("\n✅ 前處理測試完成")
