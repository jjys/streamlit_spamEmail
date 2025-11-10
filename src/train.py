"""
模型訓練腳本
"""

from model import SpamClassifier
from sklearn.model_selection import train_test_split
import os


def main():
    print("=" * 60)
    print("🚀 垃圾郵件分類器訓練程式")
    print("=" * 60)
    print()
    
    # 初始化分類器
    classifier = SpamClassifier()
    
    # 載入資料
    print("📊 載入資料集...")
    data_path = '../data/sms_spam_no_header.csv'
    
    if not os.path.exists(data_path):
        print(f"❌ 找不到資料檔案: {data_path}")
        print("請確保 sms_spam_no_header.csv 在 data/ 目錄中")
        return
    
    df = classifier.load_data(data_path)
    print(f"✅ 資料集大小: {len(df)} 筆")
    print(f"   - Ham (正常郵件): {len(df[df['label']=='ham'])} 筆")
    print(f"   - Spam (垃圾郵件): {len(df[df['label']=='spam'])} 筆")
    print()
    
    # 準備資料
    print("🔧 準備訓練資料...")
    df = classifier.prepare_data(df)
    print("✅ 資料前處理完成")
    print()
    
    # 分割資料
    print("✂️  分割訓練集與測試集 (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_message'],
        df['label'],
        test_size=0.2,
        random_state=42,
        stratify=df['label']  # 保持標籤比例
    )
    print(f"✅ 訓練集: {len(X_train)} 筆")
    print(f"   測試集: {len(X_test)} 筆")
    print()
    
    # 訓練模型
    print("🎓 開始訓練模型...")
    print("-" * 60)
    classifier.train(X_train, y_train)
    print("-" * 60)
    print()
    
    # 評估模型
    print("📈 評估模型效能...")
    metrics = classifier.evaluate(X_test, y_test)
    
    print()
    print("=" * 60)
    print("📊 模型效能指標")
    print("=" * 60)
    print(f"準確率 (Accuracy):  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"精確率 (Precision): {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"召回率 (Recall):    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"F1 分數 (F1-Score): {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
    print("=" * 60)
    print()
    
    # 檢查是否達到要求
    if metrics['accuracy'] >= 0.95:
        print("✅ 恭喜！模型準確率達到 95% 以上的要求")
    else:
        print(f"⚠️  警告: 模型準確率 ({metrics['accuracy']*100:.2f}%) 未達到 95% 要求")
        print("   建議: 調整模型參數或增加特徵")
    print()
    
    # 儲存模型
    print("💾 儲存模型...")
    classifier.save_model()
    print()
    
    # 測試預測
    print("🧪 測試預測功能...")
    print("-" * 60)
    
    test_messages = [
        "Congratulations! You've won a $1000 prize. Call now!",
        "Hi, can we meet tomorrow at 3pm for coffee?",
        "URGENT! Your account will be closed. Click here now!"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        result = classifier.predict(msg)
        print(f"\n測試 {i}:")
        print(f"訊息: {msg}")
        print(f"預測: {result['prediction'].upper()} "
              f"(spam: {result['spam_probability']:.2%}, "
              f"ham: {result['ham_probability']:.2%})")
    
    print()
    print("-" * 60)
    print()
    print("✨ 訓練完成!")
    print()
    print("📌 下一步:")
    print("   1. 執行 'streamlit run app.py' 啟動網頁應用")
    print("   2. 在瀏覽器測試分類器功能")
    print("   3. 準備部署到 Streamlit Cloud")
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  訓練被使用者中斷")
    except Exception as e:
        print(f"\n\n❌ 訓練過程發生錯誤: {e}")
        import traceback
        traceback.print_exc()
