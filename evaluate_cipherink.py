# evaluate_cipherink.py
import os
import csv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from app import bootstrap, analyze_all
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# ---------- CONFIG ----------
EVAL_ROOT = "Data/eval"   # eval/A, eval/B, eval/C, eval/D, eval/E, eval/Outsider
KNOWN_AUTHORS = ["Student A", "Student B", "Student C", "Student D", "Student E"]

# ---------- HELPERS ----------
def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def label_from_folder(folder_name):
    if folder_name.lower() == "outsider":
        return "Outsider"
    return f"Student {folder_name.upper()}"

# ---------- LOAD MODEL ----------
bootstrap()  # loads profiles from data/students/*

y_true = []
y_pred = []
y_score = []   # outsider probability for AUC
rows = []

for folder in sorted(os.listdir(EVAL_ROOT)):
    folder_path = os.path.join(EVAL_ROOT, folder)
    if not os.path.isdir(folder_path):
        continue

    true_label = label_from_folder(folder)

    for fn in sorted(os.listdir(folder_path)):
        if not fn.endswith(".txt"):
            continue

        path = os.path.join(folder_path, fn)
        text = read_text(path)

        result, err = analyze_all(text)
        if err:
            print(f"Skipped {path}: {err}")
            continue

        pred_label = "Outsider" if result["is_outsider"] else result["top_candidate"]
        outsider_score = result["probabilities"].get("Outsider", 0.0) / 100.0

        y_true.append(1 if true_label == "Outsider" else 0)
        y_pred.append(1 if pred_label == "Outsider" else 0)
        y_score.append(outsider_score)

        rows.append({
            "file": path,
            "true_label": true_label,
            "pred_label": pred_label,
            "top_candidate": result["top_candidate"],
            "top_probability": result["top_probability"],
            "confidence": result["confidence"],
            "is_outsider": result["is_outsider"],
            "best_student_llr": result["best_student_llr"],
            "outsider_score": outsider_score,
        })

# ---------- METRICS ----------
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)

try:
    auc = roc_auc_score(y_true, y_score)
except Exception:
    auc = None

print("\n=== RESULTS ===")
print(f"Accuracy : {acc:.4f}")
print(f"Precision : {prec:.4f}")
print(f"Recall    : {rec:.4f}")
print(f"F1-score  : {f1:.4f}")
print(f"AUC-ROC   : {auc:.4f}" if auc is not None else "AUC-ROC   : not available")

# ---------- SAVE PREDICTIONS ----------
with open("cipherink_eval_predictions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
    if rows:
        writer.writeheader()
        writer.writerows(rows)

# Convert the existing 'rows' list into a DataFrame
df = pd.DataFrame(rows)
labels = sorted(df['true_label'].unique())
cm = confusion_matrix(df['true_label'], df['pred_label'], labels=labels)

# Plot the matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.ylabel('Actual Author')
plt.xlabel('Predicted Author')
plt.title('CipherInk Confusion Matrix')
plt.tight_layout()

# Save the image for your research paper!
plt.savefig('cipherink_confusion_matrix.png')
print("\nSaved visual matrix to: cipherink_confusion_matrix.png")

print("\nSaved: cipherink_eval_predictions.csv")
