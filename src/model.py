"""
機器學習模型模組
"""

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from preprocessing import TextPreprocessor


class SpamClassifier:
    """垃圾郵件分類器"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = MultinomialNB()
        self.is_trained = False
    
    def load_data(self, filepath):
        """載入資料集"""
        try:
            # 使用逗號分隔，並且有標題行
            df = pd.read_csv(filepath, encoding='latin-1')
            
            # 如果沒有標題，使用預設的列名
            if len(df.columns) < 2:
                df = pd.read_csv(filepath, sep='\t', names=['label', 'message'], encoding='latin-1')
            else:
                # 使用前兩欄
                df.columns = ['label', 'message'] + list(df.columns[2:])
                df = df[['label', 'message']]
            
            # 移除空值
            df = df.dropna()
            
            # 確保 message 欄位是字串型別
            df['message'] = df['message'].astype(str)
            df['label'] = df['label'].astype(str).str.lower().str.strip()
            
            # 移除空白訊息
            df = df[df['message'].str.strip() != '']
            
            # 只保留 ham 和 spam 標籤
            df = df[df['label'].isin(['ham', 'spam'])]
            
            # 重設索引
            df = df.reset_index(drop=True)
            
            print(f"✅ 成功載入 {len(df)} 筆資料")
            
            return df
        except Exception as e:
            print(f"❌ 載入資料失敗: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def prepare_data(self, df):
        """準備訓練資料"""
        # 複製資料框避免警告
        df = df.copy()
        
        # 前處理文字
        print("🔧 正在前處理文字...")
        df['processed_message'] = df['message'].apply(
            self.preprocessor.preprocess
        )
        
        # 轉換標籤
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        
        # 確保沒有空值
        df = df.dropna()
        
        # 移除前處理後為空或太短的資料 (至少要有內容)
        df = df[df['processed_message'].str.len() > 0]
        
        # 重設索引
        df = df.reset_index(drop=True)
        
        print(f"✅ 前處理完成，保留 {len(df)} 筆有效資料")
        
        return df
    
    def train(self, X_train, y_train):
        """訓練模型"""
        # TF-IDF 向量化
        print("📊 正在進行 TF-IDF 向量化...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # 訓練模型
        print("🎓 正在訓練 Naive Bayes 模型...")
        self.model.fit(X_train_tfidf, y_train)
        self.is_trained = True
        
        print("✅ 模型訓練完成")
    
    def evaluate(self, X_test, y_test):
        """評估模型"""
        if not self.is_trained:
            raise Exception("模型尚未訓練")
        
        # 轉換測試資料
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        # 預測
        y_pred = self.model.predict(X_test_tfidf)
        
        # 計算指標
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred)
        }
        
        return metrics
    
    def predict(self, text):
        """預測單一文字"""
        if not self.is_trained:
            raise Exception("模型尚未訓練")
        
        # 前處理
        processed_text = self.preprocessor.preprocess(text)
        
        # 向量化
        text_tfidf = self.vectorizer.transform([processed_text])
        
        # 預測
        prediction = self.model.predict(text_tfidf)[0]
        probability = self.model.predict_proba(text_tfidf)[0]
        
        return {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'spam_probability': probability[1],
            'ham_probability': probability[0]
        }
    
    def save_model(self, model_path='../models/model.pkl', 
                   vectorizer_path='../models/vectorizer.pkl'):
        """儲存模型"""
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        print(f"✅ 模型已儲存: {model_path}, {vectorizer_path}")
    
    def load_model(self, model_path='../models/model.pkl', 
                   vectorizer_path='../models/vectorizer.pkl'):
        """載入模型"""
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.is_trained = True
            print("✅ 模型已載入")
        except Exception as e:
            print(f"❌ 載入模型失敗: {e}")
            raise


# 測試程式碼
if __name__ == "__main__":
    print("🧪 測試垃圾郵件分類器...")
    
    classifier = SpamClassifier()
    
    # 測試預測功能需要先訓練模型
    print("\n💡 提示: 請先執行 train.py 訓練模型")
