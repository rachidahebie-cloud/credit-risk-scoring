import getpass

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

SQL_PATH = "../sql/queries.sql"

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

# Lire le fichier de requetes et executer chaque requete separement
with open(SQL_PATH, encoding="utf-8") as f:
    contenu = f.read()

for bloc in contenu.split(";"):
    bloc = bloc.strip()
    if not bloc:
        continue
    titre = bloc.splitlines()[0].lstrip("- ").strip()
    print("\n" + "=" * 70)
    print(titre)
    print("=" * 70)
    print(pd.read_sql(bloc, engine).to_string(index=False))