# 🏦 Scoring de Risque de Crédit — Projet Data Analyst

## 📌 Contexte

Dans le secteur bancaire, l'évaluation du risque de crédit est une étape clé du processus d'octroi de prêt. Ce projet reproduit une problématique métier réelle rencontrée par les Data Analysts en banque (risque, conformité, scoring) : **estimer la probabilité qu'un client fasse défaut sur son crédit dans les deux prochaines années**, à partir de ses caractéristiques financières et démographiques.

## 🎯 Objectif business

> Quels clients présentent un risque de défaut de paiement, et quels sont les facteurs qui expliquent le mieux ce risque ?

L'analyse vise à fournir des recommandations concrètes pour affiner une politique d'octroi de crédit : quels critères pondérer davantage, et quel seuil de score adopter pour limiter les pertes tout en restant compétitif commercialement.

## 📊 Dataset

- **Source** : [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit) (Kaggle)
- **Volume** : ~150 000 clients
- **Variable cible** : `SeriousDlqin2yrs` (défaut de paiement grave dans les 2 ans)
- **Variables explicatives** : revenu mensuel, taux d'endettement, nombre de retards de paiement passés, âge, nombre de crédits ouverts, nombre de personnes à charge, etc.

## 🛠️ Méthodologie

1. **Nettoyage des données** — traitement des valeurs manquantes et aberrantes (SQL + Python)
2. **Analyse exploratoire (SQL)** — requêtes avec CTE et window functions pour calculer le taux de défaut par segment (âge, revenu, ancienneté de crédit)
3. **Analyse exploratoire (Python)** — visualisation des distributions et corrélations avec la variable cible
4. **Dashboard** — tableau de bord interactif (Power BI / Tableau Public) présentant les KPIs de risque par segment
5. **Modélisation** — régression logistique (interprétable, standard réglementaire en banque) et Random Forest en comparaison, évalués par AUC-ROC et matrice de confusion
6. **Interprétation** — analyse de l'importance des variables (feature importance) et recommandations métier

## 📈 Résultats clés

*(à compléter au fur et à mesure de l'avancement)*

| Métrique | Régression logistique | Random Forest |
|---|---|---|
| AUC-ROC | — | — |
| Précision | — | — |
| Rappel | — | — |

**Principaux enseignements :**
- —
- —
- —

## 📁 Structure du repo

```
credit-risk-scoring/
├── data/
│   ├── raw/                # Données brutes (non versionnées, voir .gitignore)
│   └── processed/          # Données nettoyées
├── sql/
│   └── queries.sql         # Requêtes d'exploration (CTE, window functions)
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_modeling.ipynb
├── dashboard/
│   └── credit_risk_dashboard.pbix   # ou lien Tableau Public
├── reports/
│   └── recommandations.md
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/<ton-pseudo>/credit-risk-scoring.git
cd credit-risk-scoring
pip install -r requirements.txt
```

## 🚀 Utilisation

```bash
# Lancer l'exploration SQL
sqlite3 data/processed/credit.db < sql/queries.sql

# Lancer les notebooks dans l'ordre
jupyter notebook notebooks/
```

## 🧰 Compétences démontrées

- **SQL** : jointures, CTE, window functions, agrégations
- **Python** : pandas, numpy, matplotlib/seaborn, scikit-learn
- **Data visualisation** : Power BI / Tableau
- **Machine Learning** : classification binaire, évaluation de modèles (AUC-ROC), interprétabilité
- **Communication** : traduction de résultats techniques en recommandations business

## 👤 Auteur

*(ton nom, LinkedIn, portfolio)*

---
*Projet réalisé dans le cadre d'une préparation active à un poste de Data Analyst, avec une orientation secteur bancaire (risque de crédit, scoring).*
