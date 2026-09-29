import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, roc_curve, classification_report,
    confusion_matrix, ConfusionMatrixDisplay,
)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
sns.set_theme(style="whitegrid")

CSV_PATH = "../data/processed/credit_data_clean.csv"
OUT_DIR = "../reports/figures"

import os
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# 1. Chargement et separation features / cible
# ============================================================
df = pd.read_csv(CSV_PATH, index_col=0)

X = df.drop(columns="SeriousDlqin2yrs")
y = df["SeriousDlqin2yrs"]

# Split stratifie : garde la meme proportion de defauts (~6.6%) dans train et test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train : {X_train.shape[0]} lignes | Test : {X_test.shape[0]} lignes")
print(f"Taux de defaut train : {y_train.mean():.4f} | test : {y_test.mean():.4f}")

# ============================================================
# 2. Regression logistique
#    class_weight='balanced' compense le desequilibre (6.6% de defauts)
#    sans avoir besoin de sur/sous-echantillonner les donnees
# ============================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logreg = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
logreg.fit(X_train_scaled, y_train)

proba_logreg = logreg.predict_proba(X_test_scaled)[:, 1]
pred_logreg = logreg.predict(X_test_scaled)

auc_logreg = roc_auc_score(y_test, proba_logreg)
print(f"\n=== Regression logistique ===")
print(f"AUC-ROC : {auc_logreg:.4f}")
print(classification_report(y_test, pred_logreg, target_names=["Pas de defaut", "Defaut"]))

# ============================================================
# 3. Random Forest
#    Pas besoin de standardiser les variables pour un modele a base d'arbres
# ============================================================
rf = RandomForestClassifier(
    n_estimators=300, max_depth=10, class_weight="balanced",
    random_state=42, n_jobs=-1,
)
rf.fit(X_train, y_train)

proba_rf = rf.predict_proba(X_test)[:, 1]
pred_rf = rf.predict(X_test)

auc_rf = roc_auc_score(y_test, proba_rf)
print(f"\n=== Random Forest ===")
print(f"AUC-ROC : {auc_rf:.4f}")
print(classification_report(y_test, pred_rf, target_names=["Pas de defaut", "Defaut"]))

# ============================================================
# 4. Courbes ROC comparees
# ============================================================
fpr_lr, tpr_lr, _ = roc_curve(y_test, proba_logreg)
fpr_rf, tpr_rf, _ = roc_curve(y_test, proba_rf)

plt.figure(figsize=(7, 6))
plt.plot(fpr_lr, tpr_lr, label=f"Regression logistique (AUC = {auc_logreg:.3f})", linewidth=2)
plt.plot(fpr_rf, tpr_rf, label=f"Random Forest (AUC = {auc_rf:.3f})", linewidth=2)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Modele aleatoire (AUC = 0.5)")
plt.xlabel("Taux de faux positifs")
plt.ylabel("Taux de vrais positifs")
plt.title("Courbes ROC - comparaison des modeles")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/06_courbes_roc.png", dpi=150)
plt.close()
print("\nGraphique sauvegarde : courbes ROC")

# ============================================================
# 5. Matrice de confusion (Random Forest, le meilleur modele attendu)
# ============================================================
cm = confusion_matrix(y_test, pred_rf)
disp = ConfusionMatrixDisplay(cm, display_labels=["Pas de defaut", "Defaut"])
disp.plot(cmap="Blues", values_format="d")
plt.title("Matrice de confusion - Random Forest")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/07_matrice_confusion.png", dpi=150)
plt.close()
print("Graphique sauvegarde : matrice de confusion")

# ============================================================
# 6. Importance des variables (Random Forest)
# ============================================================
importances = pd.DataFrame({
    "variable": X.columns,
    "importance": rf.feature_importances_,
}).sort_values("importance", ascending=False)

plt.figure(figsize=(8, 6))
sns.barplot(data=importances, x="importance", y="variable", color="#2c3e50")
plt.title("Importance des variables - Random Forest")
plt.xlabel("Importance")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/08_importance_variables.png", dpi=150)
plt.close()
print("Graphique sauvegarde : importance des variables")

print("\nVariables les plus importantes :")
print(importances.to_string(index=False))

# ============================================================
# 7. Recapitulatif final
# ============================================================
print("\n" + "=" * 60)
print("RECAPITULATIF")
print("=" * 60)
print(f"{'Modele':<25}{'AUC-ROC':<10}")
print(f"{'Regression logistique':<25}{auc_logreg:<10.4f}")
print(f"{'Random Forest':<25}{auc_rf:<10.4f}")