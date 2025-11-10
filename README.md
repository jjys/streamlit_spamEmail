# 垃圾郵件分類系統

使用機器學習技術識別垃圾郵件的智慧型分類系統。

## 🎯 專案特色

- 🤖 使用 Naive Bayes 演算法
- 📊 達到 95%+ 準確率
- 🌐 Streamlit 網頁介面
- 📈 視覺化分析結果
- 🔧 OpenSpec 規格驅動開發

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
├── src/                    # 原始碼
│   ├── preprocessing.py    # 資料前處理
│   ├── model.py           # 模型定義
│   ├── train.py           # 訓練腳本
│   └── app.py             # Streamlit 應用
├── data/                   # 資料集
├── models/                 # 儲存的模型
├── openspec/              # 規格文件
├── requirements.txt       # Python 依賴
└── README.md             # 專案說明
```

## 📊 模型效能

- 準確率 (Accuracy): 96.5%
- 精確率 (Precision): 97.2%
- 召回率 (Recall): 85.1%
- F1 分數: 90.7%

## 🌐 線上 Demo

訪問 [Streamlit App](https://your-app.streamlit.app) 查看線上示範。

## 📝 開發說明

本專案使用 OpenSpec 進行規格驅動開發。查看 `openspec/` 目錄了解更多。

## 📄 授權

MIT License

## 👨‍💻 作者

IoT 課程 - 作業三
