import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

sns.set_theme(style="whitegrid")
COULEUR_RISQUE = "#c0392b"
COULEUR_NEUTRE = "#2c3e50"

CSV_PATH = "../data/processed/credit_data_clean.csv"
OUT_DIR = "../reports/figures"

import os
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH, index_col=0)

# ============================================================
# 1. Taux de defaut par tranche d'age
# ============================================================
bornes_age = [0, 30, 40, 50, 60, 70, 200]
labels_age = ["< 30", "30-39", "40-49", "50-59", "60-69", "70 et +"]
df["tranche_age"] = pd.cut(df["age"], bins=bornes_age, labels=labels_age, right=False)

taux_age = (
    df.groupby("tranche_age", observed=True)["SeriousDlqin2yrs"]
    .mean()
    .mul(100)
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.barplot(data=taux_age, x="tranche_age", y="SeriousDlqin2yrs", color=COULEUR_NEUTRE)
plt.title("Taux de défaut par tranche d'âge")
plt.xlabel("Tranche d'âge")
plt.ylabel("Taux de défaut (%)")
for i, v in enumerate(taux_age["SeriousDlqin2yrs"]):
    plt.text(i, v + 0.2, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_taux_defaut_par_age.png", dpi=150)
plt.close()
print("Graphique 1 sauvegardé : taux de défaut par âge")

# ============================================================
# 2. Taux de defaut par decile d'utilisation du credit renouvelable
# ============================================================
df["decile_utilisation"] = pd.qcut(
    df["RevolvingUtilizationOfUnsecuredLines"], 10, labels=range(1, 11), duplicates="drop"
)

taux_util = (
    df.groupby("decile_utilisation", observed=True)["SeriousDlqin2yrs"]
    .mean()
    .mul(100)
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.lineplot(
    data=taux_util, x="decile_utilisation", y="SeriousDlqin2yrs",
    marker="o", color=COULEUR_RISQUE, linewidth=2,
)
plt.title("Taux de défaut par décile d'utilisation du crédit renouvelable")
plt.xlabel("Décile (1 = utilisation la plus faible, 10 = la plus forte)")
plt.ylabel("Taux de défaut (%)")
plt.xticks(range(1, 11))
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_taux_defaut_par_decile_utilisation.png", dpi=150)
plt.close()
print("Graphique 2 sauvegardé : taux de défaut par décile d'utilisation")

# ============================================================
# 3. Impact des retards de plus de 90 jours
# ============================================================
def categoriser_retards(n):
    if n == 0:
        return "0 retard"
    elif n == 1:
        return "1 retard"
    elif n == 2:
        return "2 retards"
    else:
        return "3 retards ou plus"

df["cat_retard_90j"] = df["NumberOfTimes90DaysLate"].apply(categoriser_retards)
ordre_retards = ["0 retard", "1 retard", "2 retards", "3 retards ou plus"]

taux_retard = (
    df.groupby("cat_retard_90j", observed=True)["SeriousDlqin2yrs"]
    .mean()
    .mul(100)
    .reindex(ordre_retards)
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.barplot(data=taux_retard, x="cat_retard_90j", y="SeriousDlqin2yrs", color=COULEUR_RISQUE)
plt.title("Taux de défaut selon l'historique de retards de plus de 90 jours")
plt.xlabel("Nombre de retards de plus de 90 jours")
plt.ylabel("Taux de défaut (%)")
for i, v in enumerate(taux_retard["SeriousDlqin2yrs"]):
    plt.text(i, v + 1, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_taux_defaut_par_retards_90j.png", dpi=150)
plt.close()
print("Graphique 3 sauvegardé : impact des retards de plus de 90 jours")

# ============================================================
# 4. Courbe de gain (part cumulee des defauts captures)
# ============================================================
df_tri = df.sort_values("RevolvingUtilizationOfUnsecuredLines", ascending=False).reset_index(drop=True)
df_tri["decile_cible"] = pd.qcut(df_tri.index, 10, labels=range(1, 11))

gain = (
    df_tri.groupby("decile_cible", observed=True)["SeriousDlqin2yrs"]
    .sum()
    .reset_index(name="nb_defauts")
)
gain["pct_cumule"] = 100 * gain["nb_defauts"].cumsum() / gain["nb_defauts"].sum()
# Ligne de reference : ciblage aleatoire (10%, 20%, ... 100%)
gain["ciblage_aleatoire"] = gain["decile_cible"].astype(int) * 10

plt.figure(figsize=(8, 5))
plt.plot(gain["decile_cible"].astype(int), gain["pct_cumule"], marker="o",
         color=COULEUR_RISQUE, linewidth=2, label="Ciblage par utilisation du crédit")
plt.plot(gain["decile_cible"].astype(int), gain["ciblage_aleatoire"], linestyle="--",
         color="gray", label="Ciblage aléatoire (référence)")
plt.title("Courbe de gain : part des défauts captés par ciblage")
plt.xlabel("% de clients ciblés (par décile)")
plt.ylabel("% de défauts captés (cumulé)")
plt.xticks(range(1, 11), [f"{i*10}%" for i in range(1, 11)])
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_courbe_de_gain.png", dpi=150)
plt.close()
print("Graphique 4 sauvegardé : courbe de gain")

# ============================================================
# 5. Heatmap de corrélation avec la variable cible
# ============================================================
colonnes_numeriques = df.select_dtypes(include="number").columns
correlations = df[colonnes_numeriques].corr()[["SeriousDlqin2yrs"]].sort_values(
    "SeriousDlqin2yrs", ascending=False
)

plt.figure(figsize=(5, 7))
sns.heatmap(correlations, annot=True, fmt=".2f", cmap="RdBu_r", center=0, cbar=False)
plt.title("Corrélation de chaque variable avec le défaut de paiement")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_correlations.png", dpi=150)
plt.close()
print("Graphique 5 sauvegardé : corrélations")

print(f"\nTous les graphiques sont dans {OUT_DIR}/")