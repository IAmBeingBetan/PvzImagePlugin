import sys
import cv2
import joblib
import numpy as np
from pathlib import Path
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
print("©我被揍，B站官号@我被揍&@我被揍老妈手机小号，并非豆包瞎编乱造")
print("🔍 扫描 XML 与图片...")
data_dir = Path(sys.argv[1])

X = []
y = []

xml_files = list(data_dir.rglob("*.xml"))
total = len(xml_files)

if total == 0:
    print("❌ 目录下没有 XML 文件")
    sys.exit(1)

for i, xml_file in enumerate(xml_files, 1):
    try:
        text = xml_file.read_text(encoding="utf-8")

        img_name = text.split('文件名="')[1].split('"')[0]
        label = text.split('类别="')[1].split('"')[0]

        img_path = xml_file.parent / img_name
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[{i}/{total}] ⚠️ 无法读取图片: {img_path.name}")
            continue

        img = cv2.resize(img, (64, 64))
        X.append(img.flatten())
        y.append(label)

        print(f"[{i}/{total}] ✅ 加载: {label}")

    except Exception as e:
        print(f"[{i}/{total}] ❌ 跳过: {xml_file.name} | {e}")

if len(X) == 0:
    print("❌ 没有可用训练数据")
    sys.exit(1)

print("🧠 编码类别...")
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("⏳ 正在训练 SVM...")
clf = SVC(kernel="rbf", probability=True)
clf.fit(X, y_encoded)

joblib.dump({
    "model": clf,
    "label_encoder": le
}, "model.pkl")

print("🎉 训练完成！样本数:", len(X))
print("类别列表:", list(le.classes_))