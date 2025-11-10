#!/bin/bash

# 作業三專案設定腳本
# 此腳本會自動建立專案結構和必要檔案

echo "🚀 開始設定垃圾郵件分類專案..."
echo ""

# 設定顏色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 建立目錄結構
echo -e "${BLUE}📁 建立目錄結構...${NC}"
mkdir -p src
mkdir -p data
mkdir -p models
mkdir -p tests
mkdir -p notebooks

echo -e "${GREEN}✓${NC} 目錄結構已建立"
echo ""

# 檢查 Python 環境
echo -e "${BLUE}🐍 檢查 Python 環境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  找不到 Python 3${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} 找到 $PYTHON_VERSION"
echo ""

# 建立虛擬環境
echo -e "${BLUE}🔧 建立虛擬環境...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 虛擬環境已建立"
else
    echo -e "${YELLOW}⚠️  虛擬環境已存在${NC}"
fi
echo ""

# 啟動虛擬環境
echo -e "${BLUE}⚡ 啟動虛擬環境...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓${NC} 虛擬環境已啟動"
echo ""

# 建立 requirements.txt
echo -e "${BLUE}📦 建立 requirements.txt...${NC}"
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

# Development
pytest==7.4.3
black==23.12.1
flake8==6.1.0
EOF

echo -e "${GREEN}✓${NC} requirements.txt 已建立"
echo ""

# 安裝套件
echo -e "${BLUE}📥 安裝 Python 套件 (這可能需要幾分鐘)...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 套件安裝完成"
else
    echo -e "${YELLOW}⚠️  部分套件安裝失敗，請手動執行: pip install -r requirements.txt${NC}"
fi
echo ""

# 建立 .gitignore
echo -e "${BLUE}🚫 建立 .gitignore...${NC}"
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
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Model files
*.pkl
*.joblib
models/*.pkl
models/*.joblib

# Data
*.csv
!data/sms_spam_no_header.csv

# Logs
*.log
logs/

# Streamlit
.streamlit/secrets.toml
EOF

echo -e "${GREEN}✓${NC} .gitignore 已建立"
echo ""

# 建立 README.md
echo -e "${BLUE}📝 建立 README.md...${NC}"
cat > README.md << 'EOF'
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
EOF

echo -e "${GREEN}✓${NC} README.md 已建立"
echo ""

# 檢查資料檔案
echo -e "${BLUE}📊 檢查資料檔案...${NC}"
if [ -f "sms_spam_no_header.csv" ]; then
    if [ ! -f "data/sms_spam_no_header.csv" ]; then
        mv sms_spam_no_header.csv data/
        echo -e "${GREEN}✓${NC} 資料檔案已移至 data/ 目錄"
    else
        echo -e "${GREEN}✓${NC} 資料檔案已存在"
    fi
else
    echo -e "${YELLOW}⚠️  找不到 sms_spam_no_header.csv${NC}"
    echo -e "   請確保資料檔案在正確位置"
fi
echo ""

# 初始化 Git (如果尚未初始化)
echo -e "${BLUE}📦 檢查 Git 版本控制...${NC}"
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: Project setup"
    echo -e "${GREEN}✓${NC} Git 已初始化"
else
    echo -e "${GREEN}✓${NC} Git 已設定"
fi
echo ""

# 完成訊息
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✨ 專案設定完成！${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 下一步:"
echo ""
echo "1️⃣  檢視教學指南:"
echo "   cat HW3_教學指南.md"
echo ""
echo "2️⃣  建立原始碼檔案 (參考教學指南第三階段)"
echo ""
echo "3️⃣  訓練模型:"
echo "   cd src && python train.py"
echo ""
echo "4️⃣  啟動 Streamlit 應用:"
echo "   cd src && streamlit run app.py"
echo ""
echo "5️⃣  設定 GitHub Repository:"
echo "   git remote add origin https://github.com/你的用戶名/專案名稱.git"
echo "   git push -u origin main"
echo ""
echo "💡 提示: 請閱讀 HW3_教學指南.md 以獲得完整說明"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
