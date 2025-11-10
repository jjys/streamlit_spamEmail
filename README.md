# 雙語垃圾郵件分類系統 (Bilingual Spam Email Classifier)

使用機器學習和規則引擎技術識別中英文垃圾郵件的智慧型分類系統。

## 🎯 專案特色

- 🌏 **雙語支援**：自動檢測中文、英文、混合語言
- 🤖 **混合AI模型**：ML模型 (70%) + 規則引擎 (30%)
- 📊 **高準確率**：英文 95%+，中文約 90%
- 🌐 **Streamlit 網頁介面**：直觀易用的互動介面
- 📈 **視覺化分析**：即時顯示分類結果和信心度
- 🔧 **OpenSpec 規格驅動開發**：完整的開發規範

## 🚀 快速開始

### 安裝依賴

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 安裝套件
pip install -r requirements.txt
```

### 訓練模型

```bash
cd src
python train.py
```

### 啟動網頁應用

```bash
cd src
streamlit run app.py
```

## 📂 專案結構

```
├── src/                        # 原始碼
│   ├── preprocessing.py        # 英文資料前處理
│   ├── preprocessing_zh.py     # 中文資料前處理
│   ├── model.py               # 英文 ML 模型
│   ├── model_bilingual.py     # 雙語分類器 (混合模型)
│   ├── train.py               # 訓練腳本
│   └── app.py                 # Streamlit 網頁應用
├── data/                       # 資料集
│   └── sms_spam_no_header.csv # SMS 垃圾郵件資料集
├── models/                     # 儲存的模型
│   ├── model.pkl              # 訓練好的 ML 模型
│   └── vectorizer.pkl         # TF-IDF 向量化器
├── openspec/                  # OpenSpec 規格文件
├── requirements.txt           # Python 依賴套件
├── HW3_教學指南.md            # 完整教學文件
├── 作業檢查清單.md            # 進度追蹤清單
├── 指令速查表.md              # 快速參考指令
└── README.md                  # 專案說明
```

## 📊 模型效能

### 英文垃圾郵件檢測（ML 模型 + 規則）
- 準確率 (Accuracy): 96.5%
- 精確率 (Precision): 97.2%
- 召回率 (Recall): 85.1%
- F1 分數: 90.7%
- 方法: Naive Bayes + 規則引擎混合 (70%/30%)

### 中文垃圾郵件檢測（規則引擎）
- 方法: 關鍵字匹配 + 特徵評分
- 準確率: 約 90%
- 支援: 繁體中文、簡體中文
- 特色: 即時檢測，無需訓練

## 🌐 線上 Demo

訪問 [Streamlit App](https://streamlit-spamemail.streamlit.app) 查看線上示範。

## 🧪 測試範例

### 中文垃圾郵件
```
✅ "恭喜您中獎了！請立即點擊領取100萬獎金！" → SPAM (100%)
✅ "限時優惠！免費送！立即下載領取大獎！" → SPAM (70%)
✅ "你好，明天下午三點我們可以討論專案嗎？" → HAM (100%)
```

### 英文垃圾郵件
```
✅ "Congratulations! You've won $1000! Call now!" → SPAM (54.71%)
✅ "FREE FREE FREE! Click here now!" → SPAM (58.17%)
✅ "Hi John, can we meet tomorrow at 3pm?" → HAM (98.75%)
```

## 🎨 功能特色

### 語言自動檢測
- 自動識別中文、英文、混合語言
- 根據語言選擇最佳分類策略

### 混合分類策略
- **中文**: 規則引擎（關鍵字 + 特徵評分）
- **英文**: ML模型 (70%) + 規則引擎 (30%)
- **混合**: 綜合評估多種方法

### 視覺化介面
- 即時顯示分析結果
- 信心度百分比
- 分類機率圖表
- 處理建議

## 📝 開發說明

本專案使用 OpenSpec 進行規格驅動開發。查看 `openspec/` 目錄了解更多。

## 📄 授權

MIT License

## 👨‍💻 作者

IoT 課程 - 作業三
