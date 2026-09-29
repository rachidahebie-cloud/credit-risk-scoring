import getpass

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

CSV_PATH = "../data/processed/credit_data_clean.csv"


mot_de_passe = getpass.getpass("Mot de passe MySQL (root) : ")

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=mot_de_passe,
    host="localhost",
    port=3306,
    database="credit_scoring",
)
engine = create_engine(url)

# Charger le CSV nettoye
df = pd.read_csv(CSV_PATH, index_col=0)

# Noms de colonnes sans tiret (plus simples a utiliser en SQL)
df.columns = [c.replace("-", "_") for c in df.columns]
df.index.name = "client_id"

# Ecrire dans MySQL (table 'credit', remplacee si elle existe deja)
df.to_sql("credit", engine, if_exists="replace", index=True, chunksize=10000)

nb = pd.read_sql("SELECT COUNT(*) AS nb_lignes FROM credit", engine)
print(f"Import termine : {nb['nb_lignes'][0]} lignes dans la table credit")