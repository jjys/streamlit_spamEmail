# Notebooks 使用說明

這個目錄包含兩個 Jupyter Notebooks，展示完整的模型訓練和評估流程。

## 📓 Notebooks 清單

### 1. `model_training.ipynb` - 模型訓練
展示完整的模型訓練流程，包括：

- **資料載入與探索**
  - 載入 SMS Spam Collection 資料集
  - 資料分布視覺化（標籤比例、訊息長度分析）
  
- **文字預處理**
  - 清理文字（移除標點符號、轉小寫）
  - 移除停用詞
  - 詞幹提取 (Stemming)
  - 預處理前後對比
  
- **特徵提取**
  - TF-IDF 向量化 (max_features=5000)
  - 特徵矩陣分析
  
- **模型訓練**
  - Multinomial Naive Bayes 分類器
  - 訓練集/測試集分割 (80/20)
  
- **模型評估**
  - 準確率、精確率、召回率、F1 分數
  - 性能指標視覺化
  
- **模型儲存**
  - 儲存訓練好的模型 (model.pkl)
  - 儲存向量化器 (vectorizer.pkl)
  
- **預測測試**
  - 實際案例預測展示

---

### 2. `model_evaluation.ipynb` - 性能評估
詳細的模型性能評估和視覺化分析，包括：

- **混淆矩陣 (Confusion Matrix)**
  - 視覺化展示預測結果
  - TP, TN, FP, FN 分析
  
- **ROC 曲線和 AUC**
  - ROC 曲線繪製
  - AUC 分數計算
  - 模型效能評估
  
- **Precision-Recall 曲線**
  - PR 曲線分析
  - Average Precision Score
  
- **詳細分類報告**
  - 各項指標總覽
  - 長條圖和雷達圖視覺化
  
- **錯誤分析**
  - False Positives 分析（誤判為 SPAM）
  - False Negatives 分析（漏判 SPAM）
  - 錯誤案例展示
  
- **特徵重要性**
  - 最具 SPAM 特徵的詞
  - 最具 HAM 特徵的詞
  - 特徵權重視覺化
  
- **測試案例展示**
  - 8 個實際測試案例
  - 預測結果和機率展示
  
- **總結報告**
  - 完整評估報告生成
  - 儲存為 evaluation_report.txt

---

## 🚀 使用方法

### 1. 環境準備

確保已安裝必要的套件：

```bash
cd /Users/jys922/Documents/myproject/testProject/IoT/HW3
source venv/bin/activate
pip install jupyter notebook matplotlib seaborn
```

### 2. 啟動 Jupyter Notebook

```bash
jupyter notebook
```

這會在瀏覽器中開啟 Jupyter，然後：
1. 導航到 `notebooks/` 目錄
2. 選擇要執行的 notebook

### 3. 執行順序

建議按照以下順序執行：

1. **先執行 `model_training.ipynb`**
   - 訓練模型並儲存
   - 確保 `models/model.pkl` 和 `models/vectorizer.pkl` 已生成

2. **再執行 `model_evaluation.ipynb`**
   - 載入訓練好的模型
   - 進行詳細的性能評估

### 4. 執行 Cell

在 Jupyter Notebook 中：
- 按 `Shift + Enter` 執行當前 cell 並移到下一個
- 按 `Ctrl + Enter` 只執行當前 cell
- 或使用頂部的 "Run" 按鈕

---

## 📊 預期輸出

### model_training.ipynb 的輸出：

1. **資料統計**
   - 資料集大小: 5,574 筆
   - HAM: 86.6%, SPAM: 13.4%

2. **視覺化圖表**
   - 標籤分布圖
   - 訊息長度分布圖
   - 性能指標長條圖

3. **模型性能**
   ```
   準確率 (Accuracy):  96.59%
   精確率 (Precision): 97.21%
   召回率 (Recall):    85.07%
   F1 分數:           90.69%
   ```

4. **儲存的檔案**
   - `models/model.pkl`
   - `models/vectorizer.pkl`

### model_evaluation.ipynb 的輸出：

1. **視覺化圖表**
   - 混淆矩陣熱力圖
   - ROC 曲線 (AUC ≈ 0.98)
   - Precision-Recall 曲線
   - 性能指標雷達圖
   - 特徵重要性長條圖

2. **錯誤分析**
   - 錯誤案例列表
   - False Positives/Negatives 分析

3. **特徵重要性**
   - Top 20 SPAM 關鍵詞
   - Top 20 HAM 關鍵詞

4. **測試結果**
   - 8 個測試案例的預測結果
   - 測試準確率: 100%

5. **儲存的檔案**
   - `models/evaluation_report.txt`

---

## 📝 注意事項

1. **執行環境**
   - 需要在虛擬環境中執行
   - 確保所有依賴套件已安裝

2. **資料路徑**
   - Notebooks 位於 `notebooks/` 目錄
   - 資料檔案位於 `data/` 目錄
   - 模型檔案位於 `models/` 目錄
   - 使用相對路徑 `../` 來訪問

3. **中文顯示**
   - 已設定 matplotlib 中文字體
   - macOS: PingFang TC / Arial Unicode MS
   - 如果中文顯示有問題，請檢查系統字體

4. **執行時間**
   - `model_training.ipynb`: 約 1-2 分鐘
   - `model_evaluation.ipynb`: 約 1-2 分鐘

5. **記憶體使用**
   - 資料集不大，一般電腦都能順利執行
   - 如果遇到記憶體問題，可以減少視覺化的資料點

---

## 🔧 故障排除

### 問題 1: 找不到模組
```
ModuleNotFoundError: No module named 'xxx'
```
**解決方法**: 確保已在虛擬環境中並安裝所有依賴
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 2: 找不到檔案
```
FileNotFoundError: [Errno 2] No such file or directory: '../data/...'
```
**解決方法**: 確認當前工作目錄，應該在 `notebooks/` 目錄下

### 問題 3: 中文顯示為方塊
**解決方法**: 修改 matplotlib 字體設定
```python
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
```

### 問題 4: Jupyter Notebook 無法啟動
**解決方法**: 安裝 Jupyter
```bash
pip install jupyter notebook
```

---

## 📚 相關資源

- **專案報告**: `../專案報告.pdf`
- **GitHub 倉庫**: https://github.com/jjys/streamlit_spamEmail
- **Streamlit 應用**: `../src/app.py`
- **模型程式碼**: `../src/model.py`
- **預處理程式碼**: `../src/preprocessing.py`

---

## ✅ 檢查清單

執行完 notebooks 後，確認以下項目：

- [ ] `model_training.ipynb` 所有 cells 執行成功
- [ ] `model_evaluation.ipynb` 所有 cells 執行成功
- [ ] 看到所有視覺化圖表
- [ ] 模型性能指標正確顯示
- [ ] `models/model.pkl` 已生成
- [ ] `models/vectorizer.pkl` 已生成
- [ ] `models/evaluation_report.txt` 已生成

---

## 💡 提示

- 建議從頭到尾執行所有 cells，以確保變數正確初始化
- 可以修改測試案例來測試不同的訊息
- 視覺化圖表可以另存為圖片檔案
- 評估報告可以複製到作業文件中

---

**製作日期**: 2025年11月10日  
**作者**: jjys  
**專案**: 雙語垃圾郵件分類系統
