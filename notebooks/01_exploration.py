import pandas as pd

# Charger le dataset
df = pd.read_csv("../data/raw/cs-training.csv", index_col=0)

# nombre de valeurs non null
print(df.count())

# Options d'affichage
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Premier aperçu
print("Dimensions :", df.shape)
print("\nColonnes :")
print(df.columns.tolist())

print("\nPremières lignes :")
print(df.head())

print("\nInformations générales :")
print(df.info())

print("\nRépartition de la variable cible :")
print(df["SeriousDlqin2yrs"].value_counts())
print(df["SeriousDlqin2yrs"].value_counts(normalize=True))

print("\nStatistiques descriptives :")
print(df.describe())

# ============================================================
# Analyse générale des données
# ============================================================

# Le dataset contient 150 000 observations et 11 variables.

# ------------------------------------------------------------
# Valeurs manquantes
# ------------------------------------------------------------

# MonthlyIncome contient 120 269 valeurs renseignées sur 150 000.
# Il y a donc 29 731 valeurs manquantes (environ 19,8 %).
# NumberOfDependents contient 146 076 valeurs renseignées.
# Il y a donc 3 924 valeurs manquantes (environ 2,6 %).

# ------------------------------------------------------------
# Variable age
# ------------------------------------------------------------

# L'âge minimum est de 0, ce qui est incohérent pour cette variable.
# Cette valeur devra être vérifiée et probablement traitée.
#
# La médiane est de 52 ans et les quartiles sont :
# Q1 = 41 ans et Q3 = 63 ans.
# Ainsi, 50 % des observations se situent entre 41 et 63 ans.
#
# Le maximum est de 109 ans. Cette valeur est très éloignée
# de la zone centrale et doit donc être vérifiée comme
# valeur potentiellement aberrante.
#
# L'écart-type est de 14,77 ans, ce qui indique une dispersion
# relativement importante des âges autour de la moyenne (52,3 ans).

# ------------------------------------------------------------
# RevolvingUtilizationOfUnsecuredLines
# ------------------------------------------------------------

# Cette variable présente une forte asymétrie.
# La médiane est de 0,154 et Q3 est de 0,559,
# alors que le maximum atteint 50 708.
#
# Cette valeur maximale est extrêmement éloignée des quartiles
# et peut donc correspondre à une valeur aberrante.
#
# L'écart-type est également très élevé (249,76),
# ce qui confirme une forte dispersion des valeurs.

# ------------------------------------------------------------
# Variables concernant les retards de paiement
# ------------------------------------------------------------

# NumberOfTime30-59DaysPastDueNotWorse,
# NumberOfTimes90DaysLate et
# NumberOfTime60-89DaysPastDueNotWorse
# présentent une distribution très concentrée autour de 0.
#
# Pour ces trois variables, Q1, la médiane et Q3 sont égaux à 0,
# alors que le maximum atteint 98.
#
# Ces valeurs maximales sont donc très éloignées de la majorité
# des observations et doivent être vérifiées comme valeurs
# potentiellement aberrantes ou comme valeurs codées
# spécifiquement dans le dataset.

def detect_outliers_iqr(df):
    results = {}

    # Sélectionner uniquement les colonnes numériques
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ]

        results[column] = {
            "Q1": Q1,
            "Q3": Q3,
            "IQR": IQR,
            "borne_basse": lower_bound,
            "borne_haute": upper_bound,
            "nombre_outliers": len(outliers)
        }

    return results

outliers = detect_outliers_iqr(df)

for column, result in outliers.items():
    print(f"\n--- {column} ---")
    print(f"Q1 : {result['Q1']}")
    print(f"Q3 : {result['Q3']}")
    print(f"IQR : {result['IQR']}")
    print(f"Borne basse : {result['borne_basse']}")
    print(f"Borne haute : {result['borne_haute']}")
    print(f"Nombre de valeurs aberrantes : {result['nombre_outliers']}")

for column, result in outliers.items():
        print(f"\n--- {column} ---")

        # Récupérer les bornes
        lower = result["borne_basse"]
        upper = result["borne_haute"]

        # Sélectionner les valeurs aberrantes
        values = df[
            (df[column] < lower) |
            (df[column] > upper)
            ][column]

        print(values.value_counts().sort_index())