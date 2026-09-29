# Scoring de Risque de Crédit — Projet Data Analyst

## Contexte

Dans le secteur bancaire, l'évaluation du risque de crédit constitue une étape importante dans l'octroi de prêts.

Ce projet reproduit une problématique de scoring de risque de crédit à partir du dataset *Give Me Some Credit*. L'objectif est d'analyser les caractéristiques des clients, d'identifier les facteurs associés au défaut de paiement et de construire des modèles permettant de distinguer les clients présentant un risque de défaut.

## Objectif business

**Quels facteurs sont les plus associés au risque de défaut de paiement et comment peuvent-ils contribuer à l'évaluation du risque client ?**

L'analyse combine exploration des données, SQL, visualisation et machine learning afin de produire des résultats exploitables pour l'analyse du risque de crédit.

## Dataset

- **Source :** [Give Me Some Credit — Kaggle](https://www.kaggle.com/c/GiveMeSomeCredit)
- **Volume :** environ 150 000 observations
- **Variable cible :** `SeriousDlqin2yrs`
- **Problématique :** prédire la présence d'un défaut de paiement grave dans les deux prochaines années.

### Principales variables

Le dataset contient notamment des informations relatives à :

- l'âge ;
- l'endettement ;
- le revenu mensuel ;
- l'utilisation du crédit renouvelable ;
- le nombre de crédits ouverts ;
- les retards de paiement ;
- le nombre de personnes à charge.

## Méthodologie

### 1. Exploration des données

Analyse de la structure du dataset, des distributions des variables et de la variable cible.

### 2. Nettoyage des données

Traitement et préparation des données avec Python afin d'obtenir un jeu de données exploitable pour les analyses et la modélisation.

### 3. Analyse SQL

Exploration des données avec SQL afin d'étudier les taux de défaut selon différents profils et indicateurs financiers.

### 4. Analyse exploratoire

Utilisation de Python, Pandas, Matplotlib et Seaborn pour analyser les distributions, les corrélations et les relations avec la variable cible.

### 5. Visualisation

Création de visualisations permettant de mieux comprendre les facteurs associés au risque de défaut.

Un tableau de bord Power BI complète l'analyse avec une vue synthétique des indicateurs de risque.

### 6. Modélisation

Deux modèles de classification ont été entraînés et comparés :

- Régression logistique
- Random Forest

Les modèles sont évalués à l'aide de :

- AUC-ROC
- précision
- rappel
- F1-score
- matrice de confusion

### 7. Interprétation

Analyse de l'importance des variables du Random Forest afin d'identifier les facteurs les plus contributifs à la prédiction du risque.

## Résultats

Les données ont été séparées en deux ensembles :

- **119 784 observations** pour l'entraînement
- **29 946 observations** pour le test

La proportion de défaut est de **6,6 %** dans les deux ensembles.

### Performance des modèles

| Métrique | Régression logistique | Random Forest |
|---|---:|---:|
| AUC-ROC | 0.8481 | 0.8541 |
| Accuracy | 0.80 | 0.80 |
| Recall — Défaut | 0.73 | 0.73 |
| F1-score — Défaut | 0.33 | 0.33 |

Les deux modèles présentent des performances proches sur le jeu de test, avec une AUC-ROC d'environ 0,85.

## Variables les plus importantes

L'analyse du Random Forest met principalement en évidence les variables suivantes :

| Variable | Importance |
|---|---:|
| `RevolvingUtilizationOfUnsecuredLines` | 37,3 % |
| `NumberOfTimes90DaysLate` | 18,4 % |
| `NumberOfTime30-59DaysPastDueNotWorse` | 17,7 % |
| `NumberOfTime60-89DaysPastDueNotWorse` | 10,2 % |
| `age` | 5,2 % |
| `DebtRatio` | 3,4 % |

Les indicateurs liés à l'utilisation du crédit et aux retards de paiement représentent les variables les plus importantes dans le modèle Random Forest.

## Visualisations produites

Le projet génère notamment :

- une comparaison des courbes ROC ;
- une matrice de confusion ;
- un graphique d'importance des variables ;
- des visualisations exploratoires des données.

Les graphiques sont disponibles dans :

```text
reports/
└── figures/
    ├── 06_courbes_roc.png
    ├── 07_matrice_confusion.png
    └── 08_importance_variables.png
```

## Structure du projet

```text
credit-risk-scoring/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboards/
│   └── Analyse du risque de crédit.pbix
│
├── notebooks/
│   ├── 01_exploration.py
│   ├── 02_cleaning.py
│   ├── 03_load_mysql.py
│   ├── 04_sql_exploration.py
│   └── 05_modeling.py
│
├── reports/
│   ├── figures/
│   │   ├── 06_courbes_roc.png
│   │   ├── 07_matrice_confusion.png
│   │   └── 08_importance_variables.png
│   └── recommendations.md
│
├── sql/
│   └── queries.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Technologies utilisées

- **Python** : Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning** : Scikit-learn
- **SQL / MySQL**
- **Power BI**
- **Git / GitHub**

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/<ton-pseudo>/credit-risk-scoring.git
cd credit-risk-scoring
```

Créer et activer un environnement virtuel :

```bash
python -m venv .venv
```

Sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Exécution

Les scripts Python peuvent être exécutés depuis le dossier `notebooks` :

```bash
cd notebooks
python 01_exploration.py
python 02_cleaning.py
python 03_load_mysql.py
python 04_sql_exploration.py
python 05_modeling.py
```

Le script de modélisation génère automatiquement les graphiques dans :

```text
reports/figures/
```

## Principaux enseignements

L'analyse met en évidence l'importance des indicateurs liés à l'historique de paiement et à l'utilisation du crédit dans la prédiction du défaut.

Les variables liées aux retards de paiement figurent parmi les facteurs les plus importants du modèle, tandis que `RevolvingUtilizationOfUnsecuredLines` représente la variable ayant la plus forte importance dans le Random Forest.

Ces résultats permettent d'alimenter une réflexion métier autour de l'identification et du suivi des profils présentant un risque de défaut.

## Compétences démontrées

- **Analyse de données** : nettoyage, exploration et interprétation
- **SQL** : requêtes, agrégations, CTE et analyse de données
- **Python** : Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning** : classification binaire, Régression logistique, Random Forest
- **Évaluation de modèles** : AUC-ROC, précision, rappel, F1-score, matrice de confusion
- **Data visualisation** : Power BI
- **Analyse métier** : interprétation des résultats et formulation de recommandations
- **Gestion de projet** : Git / GitHub

## Auteur

**TIE RACHIDA HEBIE**

Étudiante en BUT Informatique
