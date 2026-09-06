import pandas as pd

# Charger le dataset
df = pd.read_csv("../data/raw/cs-training.csv", index_col=0)

# Premier aperçu
print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df.info())
print(df["SeriousDlqin2yrs"].value_counts(normalize=True))
print(df.describe())

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("../data/raw/cs-training.csv", index_col=0)

print(df.describe())