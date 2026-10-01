import sys
import cv2
import joblib
import numpy as np
print("©我被揍，B站官号@我被揍&@我被揍老妈手机小号，并非豆包瞎编乱造")
if len(sys.argv) < 2:
    print("类别:未知")
    print("置信度:0.00")
    sys.exit(1)

image_path = sys.argv[1]

try:
    data = joblib.load("model.pkl")
    clf = data["model"]
    le = data["label_encoder"]
except Exception:
    print("类别:未知")
    print("置信度:0.00")
    sys.exit(1)

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    print("类别:未知")
    print("置信度:0.00")
    sys.exit(1)

img = cv2.resize(img, (64, 64))
features = img.flatten().reshape(1, -1)

pred = clf.predict(features)[0]
prob = max(clf.predict_proba(features)[0])
label = le.inverse_transform([pred])[0]

print(f"类别:{label}")
print(f"置信度:{prob:.2f}")
