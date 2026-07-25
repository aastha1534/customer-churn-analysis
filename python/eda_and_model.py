"""
eda_and_model.py
-----------------
End-to-end EDA + Machine Learning pipeline for the Telco Customer Churn
dataset.

Steps:
  1. Load & clean data
  2. Exploratory Data Analysis (EDA) with saved charts
  3. Feature engineering + preprocessing
  4. Train/evaluate Logistic Regression & Random Forest models
  5. Save feature-importance chart + metrics summary

Run:
    python eda_and_model.py
Outputs (written to ../images/):
    churn_distribution.png
    churn_by_contract.png
    churn_by_tenure.png
    churn_by_monthly_charges.png
    correlation_heatmap.png
    feature_importance.png
    confusion_matrix.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, accuracy_score
)

sns.set_theme(style="whitegrid")
IMG_DIR = "../images/"

# ---------------------------------------------------------------- 1. LOAD
df = pd.read_csv("../data/telco_customer_churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

print("Rows:", len(df))
print(df["Churn"].value_counts(normalize=True))

# ---------------------------------------------------------------- 2. EDA
plt.figure(figsize=(5, 4))
sns.countplot(data=df, x="Churn", hue="Churn", palette=["#2ecc71", "#e74c3c"], legend=False)
plt.title("Customer Churn Distribution")
plt.tight_layout()
plt.savefig(IMG_DIR + "churn_distribution.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 4))
ct = pd.crosstab(df["Contract"], df["Churn"], normalize="index") * 100
ct.plot(kind="bar", stacked=True, color=["#2ecc71", "#e74c3c"])
plt.ylabel("% of customers")
plt.title("Churn Rate by Contract Type")
plt.tight_layout()
plt.savefig(IMG_DIR + "churn_by_contract.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 4))
sns.histplot(data=df, x="tenure", hue="Churn", multiple="stack",
             palette=["#2ecc71", "#e74c3c"], bins=24)
plt.title("Tenure Distribution by Churn Status")
plt.tight_layout()
plt.savefig(IMG_DIR + "churn_by_tenure.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="Churn", y="MonthlyCharges", hue="Churn", palette=["#2ecc71", "#e74c3c"], legend=False)
plt.title("Monthly Charges by Churn Status")
plt.tight_layout()
plt.savefig(IMG_DIR + "churn_by_monthly_charges.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 5))
num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap (Numeric Features)")
plt.tight_layout()
plt.savefig(IMG_DIR + "correlation_heatmap.png", dpi=150)
plt.close()

# ---------------------------------------------------------- 3. PREPROCESS
model_df = df.drop(columns=["customerID"]).copy()
target = (model_df["Churn"] == "Yes").astype(int)
model_df.drop(columns=["Churn"], inplace=True)

cat_cols = model_df.select_dtypes(include=["object", "str"]).columns
for col in cat_cols:
    model_df[col] = LabelEncoder().fit_transform(model_df[col])

X_train, X_test, y_train, y_test = train_test_split(
    model_df, target, test_size=0.2, random_state=42, stratify=target
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------- 4. MODELS
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced")
log_reg.fit(X_train_scaled, y_train)
lr_pred = log_reg.predict(X_test_scaled)
lr_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

rf = RandomForestClassifier(
    n_estimators=300, max_depth=8, random_state=42, class_weight="balanced"
)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:, 1]

print("\n--- Logistic Regression ---")
print("Accuracy:", round(accuracy_score(y_test, lr_pred), 3))
print("ROC-AUC :", round(roc_auc_score(y_test, lr_proba), 3))
print(classification_report(y_test, lr_pred, target_names=["Retained", "Churned"]))

print("\n--- Random Forest ---")
print("Accuracy:", round(accuracy_score(y_test, rf_pred), 3))
print("ROC-AUC :", round(roc_auc_score(y_test, rf_proba), 3))
print(classification_report(y_test, rf_pred, target_names=["Retained", "Churned"]))

# ---------------------------------------------------------- 5. OUTPUTS
importances = pd.Series(rf.feature_importances_, index=model_df.columns)
importances = importances.sort_values(ascending=False).head(12)

plt.figure(figsize=(7, 5))
sns.barplot(x=importances.values, y=importances.index, color="#3498db")
plt.title("Top 12 Feature Importances (Random Forest)")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(IMG_DIR + "feature_importance.png", dpi=150)
plt.close()

cm = confusion_matrix(y_test, rf_pred)
plt.figure(figsize=(4.5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Retained", "Churned"], yticklabels=["Retained", "Churned"])
plt.title("Confusion Matrix (Random Forest)")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(IMG_DIR + "confusion_matrix.png", dpi=150)
plt.close()

# Write a small metrics summary for the README / reports
with open("../images/model_metrics.txt", "w") as f:
    f.write("MODEL PERFORMANCE SUMMARY\n")
    f.write("==========================\n\n")
    f.write("Logistic Regression\n")
    f.write(f"  Accuracy: {accuracy_score(y_test, lr_pred):.3f}\n")
    f.write(f"  ROC-AUC : {roc_auc_score(y_test, lr_proba):.3f}\n\n")
    f.write("Random Forest\n")
    f.write(f"  Accuracy: {accuracy_score(y_test, rf_pred):.3f}\n")
    f.write(f"  ROC-AUC : {roc_auc_score(y_test, rf_proba):.3f}\n\n")
    f.write("Top features driving churn (Random Forest importance):\n")
    for feat, val in importances.items():
        f.write(f"  {feat}: {val:.3f}\n")

print("\nAll charts saved to ../images/")
