"""
雙語垃圾郵件分類器
支援中英文自動檢測和分類
"""

import re
from model import SpamClassifier
from preprocessing_zh import ChineseTextPreprocessor


class BilingualSpamClassifier:
    """雙語垃圾郵件分類器"""
    
    def __init__(self):
        # 英文分類器（已訓練好的）
        self.en_classifier = SpamClassifier()
        self.en_classifier_loaded = False
        
        # 中文前處理器
        self.zh_preprocessor = ChineseTextPreprocessor()
    
    def load_models(self, en_model_path='../models/model.pkl', 
                   en_vectorizer_path='../models/vectorizer.pkl'):
        """載入模型"""
        try:
            self.en_classifier.load_model(en_model_path, en_vectorizer_path)
            self.en_classifier_loaded = True
            print("✅ 英文模型已載入")
        except Exception as e:
            print(f"⚠️  英文模型載入失敗: {e}")
    
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
    
    def predict_chinese_rule_based(self, text):
        """基於規則的中文垃圾訊息檢測"""
        # 清理文字
        cleaned_text = self.zh_preprocessor.clean_text(text)
        
        # 檢查垃圾訊息關鍵字
        has_spam_keywords = self.zh_preprocessor.has_spam_keywords(text)
        
        # 垃圾訊息特徵評分
        spam_score = 0
        
        # 1. 包含垃圾關鍵字 (+0.5)
        if has_spam_keywords:
            spam_score += 0.5
        
        # 2. 包含多個驚嘆號 (+0.2)
        if text.count('！') + text.count('!') >= 2:
            spam_score += 0.2
        
        # 3. 包含數字（可能是金額或電話） (+0.15)
        if re.search(r'\d+', text):
            spam_score += 0.15
        
        # 4. 包含 URL 或連結提示 (+0.3)
        if re.search(r'http|www\.|點擊|連結|網址', text, re.IGNORECASE):
            spam_score += 0.3
        
        # 5. 全大寫或過多表情符號 (+0.15)
        if text.isupper() or text.count('🎉') + text.count('💰') + text.count('🎁') >= 2:
            spam_score += 0.15
        
        # 6. 文字長度異常（太短或太長） (+0.1)
        if len(cleaned_text) < 10 or len(cleaned_text) > 500:
            spam_score += 0.1
        
        # 限制在 0-1 之間
        spam_score = min(1.0, spam_score)
        ham_score = 1.0 - spam_score
        
        prediction = 'spam' if spam_score > 0.5 else 'ham'
        
        return {
            'prediction': prediction,
            'spam_probability': spam_score,
            'ham_probability': ham_score,
            'method': 'rule-based',
            'language': 'chinese'
        }
    
    def predict_english_rule_based(self, text):
        """基於規則的英文垃圾訊息檢測（後備方案）"""
        text_lower = text.lower()
        
        # 英文垃圾訊息關鍵字
        spam_keywords = [
            'winner', 'won', 'prize', 'free', 'congratulations', 'urgent',
            'click here', 'call now', 'limited time', 'act now', 'offer',
            'discount', 'guarantee', 'money back', 'risk free', 'buy now',
            'order now', 'subscribe', 'unsubscribe', 'casino', 'lottery',
            'claim', 'reward', 'bonus', 'gift', 'promotion', 'deal',
            '$$$', '!!!', 'cheap', 'lowest price', 'save money', 'earn money'
        ]
        
        spam_score = 0
        
        # 1. 檢查垃圾關鍵字
        keyword_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
        if keyword_count >= 3:
            spam_score += 0.5
        elif keyword_count >= 2:
            spam_score += 0.3
        elif keyword_count >= 1:
            spam_score += 0.2
        
        # 2. 多個驚嘆號
        exclamation_count = text.count('!')
        if exclamation_count >= 3:
            spam_score += 0.3
        elif exclamation_count >= 2:
            spam_score += 0.2
        
        # 3. 全大寫字詞
        words = text.split()
        uppercase_words = sum(1 for word in words if word.isupper() and len(word) > 2)
        if uppercase_words >= 2:
            spam_score += 0.2
        
        # 4. 包含金錢符號
        if '$' in text or '£' in text or '€' in text:
            spam_score += 0.2
        
        # 5. 包含 URL 或電話號碼
        if re.search(r'http|www\.|1-\d{3}-\d{3}', text_lower):
            spam_score += 0.2
        
        # 6. 包含典型垃圾句式
        spam_patterns = [
            r'you.{0,10}won',
            r'claim.{0,10}(now|prize|reward)',
            r'click.{0,10}(here|now)',
            r'call.{0,10}now',
            r'limited.{0,10}time'
        ]
        pattern_matches = sum(1 for pattern in spam_patterns if re.search(pattern, text_lower))
        spam_score += pattern_matches * 0.15
        
        # 限制在 0-1 之間
        spam_score = min(1.0, spam_score)
        ham_score = 1.0 - spam_score
        
        prediction = 'spam' if spam_score > 0.5 else 'ham'
        
        return {
            'prediction': prediction,
            'spam_probability': spam_score,
            'ham_probability': ham_score,
            'method': 'rule-based',
            'language': 'english'
        }
    
    def predict(self, text):
        """預測文字是否為垃圾訊息"""
        if not text or not text.strip():
            return {
                'prediction': 'ham',
                'spam_probability': 0.0,
                'ham_probability': 1.0,
                'method': 'empty-text',
                'language': 'unknown'
            }
        
        # 檢測語言
        language = self.detect_language(text)
        
        # 根據語言選擇分類方法
        if language == 'chinese':
            # 使用基於規則的中文分類
            return self.predict_chinese_rule_based(text)
        
        elif language == 'english':
            # 使用訓練好的英文模型
            if self.en_classifier_loaded:
                # ML 模型預測
                ml_result = self.en_classifier.predict(text)
                
                # 規則檢測
                rule_result = self.predict_english_rule_based(text)
                
                # 混合策略：如果任一方法判定為垃圾郵件且信心度高，就判定為垃圾
                # 或者取兩者的加權平均 (ML 權重 70%, 規則權重 30%)
                ml_weight = 0.7
                rule_weight = 0.3
                
                combined_spam_prob = (
                    ml_result['spam_probability'] * ml_weight +
                    rule_result['spam_probability'] * rule_weight
                )
                
                combined_ham_prob = 1.0 - combined_spam_prob
                
                return {
                    'prediction': 'spam' if combined_spam_prob > 0.5 else 'ham',
                    'spam_probability': combined_spam_prob,
                    'ham_probability': combined_ham_prob,
                    'method': 'ml-model+rules',
                    'language': 'english',
                    'ml_score': ml_result['spam_probability'],
                    'rule_score': rule_result['spam_probability']
                }
            else:
                # 使用規則檢測作為後備
                return self.predict_english_rule_based(text)
        
        else:  # mixed language
            # 混合語言：同時使用兩種方法，取平均
            results = []
            
            # 中文規則評分
            zh_result = self.predict_chinese_rule_based(text)
            results.append(zh_result['spam_probability'])
            
            # 英文模型或規則評分
            if self.en_classifier_loaded:
                en_result = self.en_classifier.predict(text)
                results.append(en_result['spam_probability'])
            else:
                en_result = self.predict_english_rule_based(text)
                results.append(en_result['spam_probability'])
            
            # 計算平均分數
            avg_spam_prob = sum(results) / len(results)
            avg_ham_prob = 1.0 - avg_spam_prob
            
            return {
                'prediction': 'spam' if avg_spam_prob > 0.5 else 'ham',
                'spam_probability': avg_spam_prob,
                'ham_probability': avg_ham_prob,
                'method': 'hybrid',
                'language': 'mixed'
            }


# 測試程式碼
if __name__ == "__main__":
    print("🧪 測試雙語垃圾郵件分類器...")
    
    classifier = BilingualSpamClassifier()
    
    # 嘗試載入英文模型
    try:
        classifier.load_models()
    except:
        print("⚠️  英文模型尚未訓練，僅使用規則檢測")
    
    test_messages = [
        "恭喜您中獎了！請立即點擊 http://bit.ly/xxx 領取100萬獎金！",
        "你好，明天下午三點我們可以討論一下專案進度嗎？",
        "限時優惠！免費送！立即下載領取大獎！",
        "Congratulations! You've won $1000! Call 1-800-XXX now!",
        "Hi John, can we meet tomorrow at 3pm?",
        "FREE FREE FREE! Click here now!",
        "WINNER!! As a valued customer you have been selected to receive a prize!",
        "Your order #12345 has been shipped and will arrive soon."
    ]
    
    print("\n" + "="*60)
    for i, msg in enumerate(test_messages, 1):
        result = classifier.predict(msg)
        print(f"\n測試 {i}:")
        print(f"訊息: {msg}")
        print(f"語言: {result['language']}")
        print(f"預測: {result['prediction'].upper()}")
        print(f"垃圾機率: {result['spam_probability']:.2%}")
        print(f"正常機率: {result['ham_probability']:.2%}")
        print(f"方法: {result['method']}")
        print("-"*60)
    
    print("\n✅ 測試完成")
