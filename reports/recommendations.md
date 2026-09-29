## Recommandations métier

À partir des résultats de l'analyse et des variables les plus importantes dans le modèle, plusieurs pistes peuvent être proposées pour améliorer l'évaluation du risque de crédit.

### 1. Accorder une attention particulière à l'historique de paiement

Les retards de paiement figurent parmi les variables les plus importantes du modèle. Il peut donc être pertinent d'intégrer davantage l'historique des incidents de paiement dans l'analyse du risque client.

### 2. Surveiller l'utilisation du crédit

La variable `RevolvingUtilizationOfUnsecuredLines` présente la plus forte importance dans le Random Forest. Le niveau d'utilisation du crédit constitue donc un indicateur à surveiller lors de l'évaluation du profil de risque.

### 3. Segmenter les profils de risque

Les analyses exploratoires peuvent être utilisées pour identifier différents profils de clients selon leur âge, leur niveau d'endettement, leur revenu et leur historique de paiement.

Cette segmentation permettrait d'adapter le suivi et l'analyse du risque aux caractéristiques de chaque groupe.

### 4. Utiliser le modèle comme outil d'aide à la décision

Avec une AUC-ROC d'environ 0,85 sur le jeu de test, les modèles permettent d'apporter une information complémentaire dans l'évaluation du risque.

Dans un contexte réel, le score devrait cependant être intégré à une analyse plus globale et être validé sur des données indépendantes avant toute utilisation opérationnelle.

### 5. Approfondir l'analyse avant une mise en production

Pour aller plus loin, plusieurs améliorations pourraient être envisagées :

- tester d'autres modèles de classification ;
- optimiser les hyperparamètres ;
- analyser différents seuils de classification ;
- étudier plus précisément les faux positifs et les faux négatifs ;
- mettre en place une validation croisée ;
- approfondir l'interprétabilité des prédictions.

### Synthèse

L'analyse montre que **l'historique des retards de paiement et l'utilisation du crédit** constituent des facteurs particulièrement importants dans la prédiction du défaut.

Ces résultats peuvent servir de base à une réflexion sur la segmentation des profils de risque et sur l'amélioration des outils d'aide à la décision dans le domaine du crédit.