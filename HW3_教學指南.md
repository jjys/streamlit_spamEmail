# 作業三：垃圾郵件分類系統 - 完整教學指南

## 📋 作業需求概述

本作業要求使用 **OpenSpec** 和 **AI Coding CLI** 工具來開發一個垃圾郵件分類系統。

### 核心要求
1. ✅ 建立 GitHub Repository
2. ✅ 部署 Streamlit Demo 網站
3. ✅ 使用 OpenSpec 進行規格驅動開發
4. ✅ 實作垃圾郵件分類功能

### 參考資源
- **教學影片**: [YouTube 教學播放列表](https://www.youtube.com/watch?v=FeCCYFK0TJ8&list=PLYlM4-ln5HcCoM_TcLKGL5NcOpNVJ3g7c)
- **程式碼參考**: [Hands-On AI for Cybersecurity](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity.git)
- **範例專案**: https://github.com/huanchen1107/2025ML-spamEmail
- **範例 Demo**: https://2025spamemail.streamlit.app/
- **Streamlit 部署教學**: https://www.youtube.com/watch?v=ANjiJQQIBo0

---

## 🎯 專案目標

開發一個機器學習系統，能夠：
- 分析文字內容
- 識別垃圾郵件
- 透過網頁介面提供預測服務
- 達到 95% 以上的準確率

---

## 🛠 技術堆疊

### 核心技術
- **Python 3.x**: 主要開發語言
- **scikit-learn**: 機器學習框架
- **pandas**: 資料處理
- **numpy**: 數值運算
- **Streamlit**: 網頁介面
- **NLTK**: 自然語言處理

### 開發工具
- **OpenSpec**: 規格驅動開發工具
- **Git/GitHub**: 版本控制
- **Streamlit Cloud**: 部署平台

---

## 📦 專案結構

```
HW3/
├── .github/                    # GitHub 設定
│   └── prompts/               # OpenSpec 提示詞
├── openspec/                   # OpenSpec 規格文件
│   ├── AGENTS.md              # AI 助手指引
│   ├── project.md             # 專案上下文
│   ├── specs/                 # 功能規格
│   └── changes/               # 變更提案
├── src/                        # 原始碼 (待建立)
│   ├── preprocessing.py       # 資料前處理
│   ├── model.py              # 模型訓練
│   ├── predict.py            # 預測服務
│   └── app.py                # Streamlit 應用
├── data/                       # 資料集
│   └── sms_spam_no_header.csv
├── requirements.txt            # Python 套件清單
└── README.md                  # 專案說明
```

---

## 🚀 實作步驟

### 階段一：環境設定

#### 1.1 建立 GitHub Repository

```bash
# 初始化 Git (如果還沒有)
cd /Users/jys922/Documents/myproject/testProject/IoT/HW3
git init

# 建立 .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Jupyter Notebook
.ipynb_checkpoints

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Model files
*.pkl
*.joblib

# Data (optional)
data/*.csv
!data/sms_spam_no_header.csv
EOF

# 提交到 GitHub
git add .
git commit -m "Initial commit: OpenSpec setup"
git remote add origin https://github.com/你的用戶名/spam-email-classifier.git
git branch -M main
git push -u origin main
```

#### 1.2 安裝必要工具

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 安裝 OpenSpec CLI
npm install -g openspec-cli

# 或使用 pip
pip install openspec-cli

# 驗證安裝
openspec --version
```

#### 1.3 建立 requirements.txt

```bash
cat > requirements.txt << 'EOF'
# Machine Learning
scikit-learn==1.3.2
numpy==1.26.2
pandas==2.1.3

# NLP
nltk==3.8.1

# Web Interface
streamlit==1.29.0

# Utilities
joblib==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
EOF
```

---

### 階段二：使用 OpenSpec 建立規格

#### 2.1 理解 OpenSpec 工作流

OpenSpec 採用三階段工作流：

1. **創建變更提案 (Creating Changes)**
   - 定義新功能需求
   - 撰寫規格文件

2. **實作變更 (Implementing Changes)**
   - 根據規格開發程式碼
   - 追蹤實作進度

3. **歸檔變更 (Archiving Changes)**
   - 合併規格到主文件
   - 清理變更歷史

#### 2.2 查看現有規格

```bash
# 列出所有規格
openspec spec list --long

# 查看變更歷史
openspec list

# 查看特定規格詳情
openspec spec show spam-detection
```

#### 2.3 建立新的變更提案

如果需要新增功能，例如「資料視覺化」：

```bash
# 使用 AI 助手建立提案
# 在 VS Code 中對話：
# "幫我建立一個變更提案，要新增資料視覺化功能"
```

AI 助手會：
1. 檢查 `openspec/AGENTS.md`
2. 建立 `openspec/changes/add-visualization/` 目錄
3. 產生 `proposal.md`, `tasks.md`, `design.md`
4. 建立規格變更檔案

#### 2.4 驗證提案

```bash
# 驗證提案格式
openspec validate add-visualization --strict

# 修正任何錯誤
```

---

### 階段三：實作核心功能

#### 3.1 資料前處理模組

建立 `src/preprocessing.py`:

```python
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
nltk.download('stopwords', quiet=True)

class TextPreprocessor:
    """文字前處理器"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
    
    def clean_text(self, text):
        """
        清理文字
        
        Args:
            text (str): 原始文字
            
        Returns:
            str: 清理後的文字
        """
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
        words = text.split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    def preprocess(self, text):
        """完整的前處理流程"""
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        text = self.stem_text(text)
        return text
```

#### 3.2 模型訓練模組

建立 `src/model.py`:

```python
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
        df = pd.read_csv(filepath, sep='\t', names=['label', 'message'])
        return df
    
    def prepare_data(self, df):
        """準備訓練資料"""
        # 前處理文字
        df['processed_message'] = df['message'].apply(
            self.preprocessor.preprocess
        )
        
        # 轉換標籤
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        
        return df
    
    def train(self, X_train, y_train):
        """訓練模型"""
        # TF-IDF 向量化
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # 訓練模型
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
    
    def save_model(self, model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        """儲存模型"""
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        print(f"✅ 模型已儲存: {model_path}, {vectorizer_path}")
    
    def load_model(self, model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        """載入模型"""
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.is_trained = True
        print("✅ 模型已載入")
```

#### 3.3 訓練腳本

建立 `src/train.py`:

```python
"""
模型訓練腳本
"""

from model import SpamClassifier
from sklearn.model_selection import train_test_split

def main():
    print("🚀 開始訓練垃圾郵件分類器...")
    
    # 初始化分類器
    classifier = SpamClassifier()
    
    # 載入資料
    print("📊 載入資料集...")
    df = classifier.load_data('../data/sms_spam_no_header.csv')
    print(f"資料集大小: {len(df)} 筆")
    
    # 準備資料
    print("🔧 前處理資料...")
    df = classifier.prepare_data(df)
    
    # 分割資料
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_message'],
        df['label'],
        test_size=0.2,
        random_state=42
    )
    
    # 訓練模型
    print("🎓 訓練模型...")
    classifier.train(X_train, y_train)
    
    # 評估模型
    print("📈 評估模型...")
    metrics = classifier.evaluate(X_test, y_test)
    
    print("\n" + "="*50)
    print("模型效能指標:")
    print("="*50)
    print(f"準確率 (Accuracy):  {metrics['accuracy']:.4f}")
    print(f"精確率 (Precision): {metrics['precision']:.4f}")
    print(f"召回率 (Recall):    {metrics['recall']:.4f}")
    print(f"F1 分數:           {metrics['f1_score']:.4f}")
    print("="*50)
    
    # 儲存模型
    print("\n💾 儲存模型...")
    classifier.save_model()
    
    print("\n✨ 訓練完成!")

if __name__ == "__main__":
    main()
```

#### 3.4 Streamlit 網頁應用

建立 `src/app.py`:

```python
"""
Streamlit 網頁應用
"""

import streamlit as st
import pandas as pd
from model import SpamClassifier

# 設定頁面
st.set_page_config(
    page_title="垃圾郵件分類器",
    page_icon="📧",
    layout="wide"
)

# 載入模型
@st.cache_resource
def load_classifier():
    classifier = SpamClassifier()
    try:
        classifier.load_model('model.pkl', 'vectorizer.pkl')
        return classifier
    except:
        st.error("❌ 無法載入模型，請先訓練模型")
        return None

# 主標題
st.title("📧 垃圾郵件分類器")
st.markdown("---")

# 載入分類器
classifier = load_classifier()

if classifier:
    # 建立兩個欄位
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 輸入郵件內容")
        
        # 文字輸入區域
        message = st.text_area(
            "請輸入要檢測的郵件內容:",
            height=200,
            placeholder="例如: Congratulations! You've won a $1000 prize..."
        )
        
        # 預測按鈕
        if st.button("🔍 開始分析", type="primary"):
            if message:
                with st.spinner("分析中..."):
                    # 進行預測
                    result = classifier.predict(message)
                    
                    # 顯示結果
                    st.markdown("---")
                    st.header("📊 分析結果")
                    
                    # 判斷結果
                    if result['prediction'] == 'spam':
                        st.error("⚠️ 這是垃圾郵件!")
                        st.metric(
                            "垃圾郵件機率",
                            f"{result['spam_probability']:.2%}"
                        )
                    else:
                        st.success("✅ 這是正常郵件!")
                        st.metric(
                            "正常郵件機率",
                            f"{result['ham_probability']:.2%}"
                        )
                    
                    # 機率圖表
                    chart_data = pd.DataFrame({
                        '類別': ['正常郵件', '垃圾郵件'],
                        '機率': [
                            result['ham_probability'],
                            result['spam_probability']
                        ]
                    })
                    
                    st.bar_chart(chart_data.set_index('類別'))
            else:
                st.warning("⚠️ 請輸入郵件內容")
    
    with col2:
        st.header("ℹ️ 使用說明")
        st.info("""
        ### 如何使用
        1. 在左側輸入框中貼上郵件內容
        2. 點擊「開始分析」按鈕
        3. 查看分析結果
        
        ### 功能說明
        - 使用機器學習模型分析郵件
        - 提供垃圾郵件機率評分
        - 視覺化顯示分類結果
        
        ### 準確率
        - 模型準確率: >95%
        - 使用 Naive Bayes 演算法
        - 基於 5000+ 訓練樣本
        """)
        
        st.header("📌 範例")
        examples = {
            "垃圾郵件範例": "Congratulations! You've won a $1000 prize. Call now!",
            "正常郵件範例": "Hi John, can we meet tomorrow at 3pm to discuss the project?"
        }
        
        for title, text in examples.items():
            if st.button(title):
                st.session_state.example = text

# 側邊欄
with st.sidebar:
    st.header("🎯 專案資訊")
    st.markdown("""
    **作業三：垃圾郵件分類系統**
    
    - 使用 OpenSpec 開發
    - 機器學習分類器
    - Streamlit 網頁介面
    
    [GitHub Repository](#)
    """)
    
    st.markdown("---")
    st.markdown("© 2025 IoT 課程作業")
```

---

### 階段四：訓練和測試

#### 4.1 安裝依賴

```bash
# 啟動虛擬環境
source venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

#### 4.2 訓練模型

```bash
# 進入 src 目錄
cd src

# 執行訓練
python train.py
```

預期輸出:
```
🚀 開始訓練垃圾郵件分類器...
📊 載入資料集...
資料集大小: 5574 筆
🔧 前處理資料...
🎓 訓練模型...
✅ 模型訓練完成
📈 評估模型...

==================================================
模型效能指標:
==================================================
準確率 (Accuracy):  0.9659
精確率 (Precision): 0.9721
召回率 (Recall):    0.8507
F1 分數:           0.9069
==================================================
```

#### 4.3 本地測試

```bash
# 啟動 Streamlit 應用
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`

---

### 階段五：部署到 Streamlit Cloud

#### 5.1 準備部署檔案

確保你的專案包含:
- ✅ `requirements.txt`
- ✅ `src/app.py`
- ✅ `model.pkl` 和 `vectorizer.pkl`
- ✅ `data/sms_spam_no_header.csv`

#### 5.2 推送到 GitHub

```bash
# 新增所有檔案
git add .

# 提交變更
git commit -m "feat: Add spam classifier with Streamlit UI"

# 推送到 GitHub
git push origin main
```

#### 5.3 部署到 Streamlit Cloud

1. 前往 https://streamlit.io/cloud
2. 使用 GitHub 帳號登入
3. 點擊「New app」
4. 選擇你的 Repository
5. 設定:
   - **Main file path**: `src/app.py`
   - **Python version**: 3.10
6. 點擊「Deploy」

等待幾分鐘，你的應用就會上線！

---

## 📊 專案檢查清單

### 必要項目
- [ ] GitHub Repository 已建立
- [ ] 使用 OpenSpec 進行開發
- [ ] 實作資料前處理模組
- [ ] 實作模型訓練模組
- [ ] 建立 Streamlit 網頁介面
- [ ] 模型準確率達到 95%
- [ ] 部署到 Streamlit Cloud
- [ ] README.md 完整說明

### 加分項目
- [ ] 資料視覺化
- [ ] 多模型比較
- [ ] API 端點
- [ ] 單元測試
- [ ] CI/CD 設定

---

## 🐛 常見問題

### Q1: OpenSpec 指令找不到
```bash
# 確認安裝
npm list -g openspec-cli

# 重新安裝
npm install -g openspec-cli
```

### Q2: NLTK 資源下載失敗
```python
# 在 Python 中手動下載
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### Q3: Streamlit 部署失敗
- 檢查 requirements.txt 版本
- 確認檔案路徑正確
- 查看 Streamlit Cloud 日誌

### Q4: 模型準確率不足 95%
- 增加訓練資料
- 調整特徵工程
- 嘗試其他演算法 (SVM, Random Forest)
- 調整超參數

---

## 📚 延伸學習

### 進階主題
1. **模型優化**
   - 超參數調整
   - 交叉驗證
   - 集成學習

2. **特徵工程**
   - Word2Vec
   - BERT Embeddings
   - N-grams

3. **部署優化**
   - Docker 容器化
   - FastAPI 後端
   - Redis 快取

### 推薦資源
- [Scikit-learn 文件](https://scikit-learn.org/)
- [Streamlit 文件](https://docs.streamlit.io/)
- [NLTK Book](https://www.nltk.org/book/)
- [OpenSpec 文件](https://openspec.dev/)

---

## 🎓 評分標準

| 項目 | 配分 | 說明 |
|------|------|------|
| GitHub Repository | 15% | 程式碼組織、版本控制 |
| OpenSpec 使用 | 20% | 規格文件完整性 |
| 模型效能 | 30% | 準確率 ≥ 95% |
| Streamlit 介面 | 20% | 使用者體驗、視覺設計 |
| 文件說明 | 15% | README、註解 |

---

## 💡 提示

1. **先讀規格再寫程式**: 遵循 OpenSpec 工作流
2. **頻繁提交**: 小步驟頻繁 commit
3. **測試驅動**: 先測試再部署
4. **參考範例**: 學習現有專案的結構
5. **詢問助手**: 善用 AI Coding CLI

---

## 🚀 開始實作

現在你已經了解整個專案的架構和實作方式，請按照以下步驟開始：

1. **建立目錄結構**
2. **設定 GitHub Repository**
3. **使用 OpenSpec 建立規格**
4. **實作核心功能**
5. **訓練和評估模型**
6. **部署到 Streamlit Cloud**

祝你順利完成作業！💪

---

**版本**: 1.0  
**更新日期**: 2025-11-10  
**作者**: AI Teaching Assistant
