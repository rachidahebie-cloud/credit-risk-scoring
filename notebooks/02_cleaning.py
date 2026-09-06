import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Charger les données brutes
df = pd.read_csv("../data/raw/cs-training.csv", index_col=0)

print(f"Avant nettoyage : {df.shape}")

# 1. Age = 0 : impossible, on supprime la/les ligne(s) concernée(s)
nb_age_zero = (df["age"] == 0).sum()
print(f"\nLignes avec age = 0 : {nb_age_zero}")
df = df[df["age"] > 0]

# 2. Les colonnes de retards de paiement avec la valeur codée 96 ou 98
#    C'est un code d'erreur historique de ce dataset, pas un vrai nombre de retards.
cols_retard = [
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate",
    "NumberOfTime60-89DaysPastDueNotWorse",
]
for col in cols_retard:
    nb_aberrant = df[col].isin([96, 98]).sum()
    print(f"Lignes avec {col} = 96 ou 98 : {nb_aberrant}")

# On supprime ces lignes (elles concernent souvent les mêmes clients sur les 3 colonnes)
mask_aberrant = df[cols_retard].isin([96, 98]).any(axis=1)
print(f"\nTotal de lignes aberrantes (retards codés 96/98) : {mask_aberrant.sum()}")
df = df[~mask_aberrant]

# 3. MonthlyIncome manquant : on impute par la médiane (plus robuste que la moyenne
#    face aux valeurs extrêmes déjà identifiées)
mediane_income = df["MonthlyIncome"].median()
df["MonthlyIncome"] = df["MonthlyIncome"].fillna(mediane_income)

# 4. NumberOfDependents manquant : on impute par 0 (hypothèse raisonnable :
#    valeur manquante = non renseigné = probablement pas de personne à charge)
df["NumberOfDependents"] = df["NumberOfDependents"].fillna(0)

# 5. RevolvingUtilizationOfUnsecuredLines et DebtRatio : on plafonne (winsorize)
#    au 99e percentile plutôt que de supprimer, pour ne pas perdre trop de lignes
for col in ["RevolvingUtilizationOfUnsecuredLines", "DebtRatio"]:
    seuil = df[col].quantile(0.99)
    nb_extreme = (df[col] > seuil).sum()
    print(f"\n{col} : {nb_extreme} valeurs au-dessus du 99e percentile ({seuil:.2f}), plafonnées")
    df[col] = df[col].clip(upper=seuil)

print(f"\nAprès nettoyage : {df.shape}")
print(f"\nNouvelle proportion de défauts :")
print(df["SeriousDlqin2yrs"].value_counts(normalize=True))

# Sauvegarder les données nettoyées
df.to_csv("../data/processed/credit_data_clean.csv")
print("\nFichier nettoyé sauvegardé dans data/processed/credit_data_clean.csv")