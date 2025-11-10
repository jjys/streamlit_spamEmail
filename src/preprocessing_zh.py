"""
中文文字前處理模組
支援中文垃圾訊息分類
"""

import re
import string

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("⚠️  jieba 未安裝，中文分詞功能將受限")


class ChineseTextPreprocessor:
    """中文文字前處理器"""
    
    def __init__(self):
        # 中文停用詞列表
        self.stop_words = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
            '一個', '上', '也', '很', '到', '說', '要', '去', '你', '會', '著', '沒有',
            '看', '好', '自己', '這', '那', '裡', '它', '嗎', '吧', '啊', '呢', '哦',
            '哈', '什麼', '怎麼', '為什麼', '誰', '哪', '哪裡', '多少', '幾', '嘛'
        ])
        
        # 垃圾訊息常見關鍵字（用於快速檢測）
        self.spam_keywords = set([
            '中獎', '恭喜', '免費', '獎金', '點擊', '領取', '優惠', '折扣',
            '限時', '立即', '馬上', '抽獎', '贏取', '獲得', '賺錢', '收益',
            '投資', '理財', '貸款', '代辦', '包過', '保證', '官方', '客服',
            '退款', '退稅', '補助', '發票', '中獎通知', '匯款', '轉帳', '銀行',
            '信用卡', '密碼', '驗證碼', '點此', '網址', '連結', '下載'
        ])
    
    def detect_language(self, text):
        """檢測文字語言"""
        if not text:
            return 'unknown'
        
        # 計算中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text.strip())
        
        if total_chars == 0:
            return 'unknown'
        
        chinese_ratio = chinese_chars / total_chars
        
        if chinese_ratio > 0.3:
            return 'chinese'
        elif chinese_ratio < 0.1:
            return 'english'
        else:
            return 'mixed'
    
    def clean_text(self, text):
        """清理文字"""
        if not isinstance(text, str):
            return ""
        
        # 移除 URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 移除 email
        text = re.sub(r'\S+@\S+', '', text)
        
        # 移除電話號碼模式
        text = re.sub(r'\d{3,4}[-]?\d{3,4}[-]?\d{3,4}', '', text)
        
        # 移除英文標點符號
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # 移除中文標點符號
        chinese_punctuation = '！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—''‛""„‟…‧﹏.'
        for char in chinese_punctuation:
            text = text.replace(char, '')
        
        # 移除多餘空白
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text):
        """中文分詞"""
        if not JIEBA_AVAILABLE:
            # 如果沒有 jieba，使用簡單的字符切割
            return list(text.replace(' ', ''))
        
        # 使用 jieba 分詞
        words = jieba.cut(text)
        return list(words)
    
    def remove_stopwords(self, words):
        """移除停用詞"""
        return [word for word in words if word not in self.stop_words and len(word.strip()) > 0]
    
    def has_spam_keywords(self, text):
        """檢查是否包含垃圾訊息關鍵字"""
        text_lower = text.lower()
        for keyword in self.spam_keywords:
            if keyword in text_lower:
                return True
        return False
    
    def preprocess(self, text):
        """完整的前處理流程"""
        if not isinstance(text, str) or not text.strip():
            return ""
        
        # 清理文字
        text = self.clean_text(text)
        
        if not text or not text.strip():
            return ""
        
        # 檢測語言
        lang = self.detect_language(text)
        
        # 如果是中文，進行分詞
        if lang in ['chinese', 'mixed']:
            words = self.tokenize(text)
            words = self.remove_stopwords(words)
            text = ' '.join(words)
        
        # 確保返回值不為空
        return text if text and text.strip() else "text"


# 測試程式碼
if __name__ == "__main__":
    print("🧪 測試中文文字前處理器...")
    
    preprocessor = ChineseTextPreprocessor()
    
    test_cases = [
        "恭喜您中獎了！請立即點擊領取100萬獎金！",
        "你好，明天下午三點可以見面嗎？",
        "限時優惠！免費送！立即下載領取！",
        "Hi, can we meet tomorrow at 3pm?"
    ]
    
    for text in test_cases:
        lang = preprocessor.detect_language(text)
        result = preprocessor.preprocess(text)
        has_spam = preprocessor.has_spam_keywords(text)
        
        print(f"\n原始: {text}")
        print(f"語言: {lang}")
        print(f"處理: {result}")
        print(f"疑似垃圾: {'是' if has_spam else '否'}")
    
    print("\n✅ 中文前處理測試完成")
