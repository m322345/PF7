# Projet OC8 - Réalisez un dashboard

Data Scientist au sein d'une société financière, nommée "Prêt à dépenser", qui propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.

L’entreprise souhaite mettre en œuvre un outil de “scoring crédit” pour calculer la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. Elle souhaite donc développer un algorithme de classification en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.)

## La mission :

1. Construire un modèle de scoring qui donnera une prédiction sur la probabilité de faillite d'un client de façon automatique.
2. Analyser les features qui contribuent le plus au modèle, d’une manière générale (feature importance globale) et au niveau d’un client (feature importance locale), afin, dans un soucis de transparence, de permettre à un chargé d’études de mieux comprendre le score attribué par le modèle.
3. Mettre en production le modèle de scoring de prédiction à l’aide d’une API et réaliser une interface de test de cette API.
4. Mettre en œuvre une approche globale MLOps de bout en bout, du tracking des expérimentations à l’analyse en production du data drift.

## Descriptif de la structure :

repertoire			| description
------------------- | -----------
.github/workflows 	| Le Workflow github qui vient lancer les tests unitaires à chaque push du projet
Api 				| Le code de l'Api qui est déployée automatiquement vers Render lors d'un push
Appli				| L'application frontend déployée automatiquement vers Streamlit
tests				| Les tests unitaires réalisés avec Pytest

Le fichier Modelisation.ipynb contient l'exploration, les tests de modélisations sauvegardées vers Mlflow et la modélisation finale.

## Les outils :

[Serveur Jupyter personnel](http://10.0.100.172:8888/)

[Serveur MlFlow personnel](http://10.0.50.72:5000/)

[Dashboard Render](https://dashboard.render.com/)

[API hébergée sur Render](https://ocp7-api.onrender.com/)

[Test de l'API hébergée sur Render](https://ocp7-api.onrender.com/docs/)

[Application hébergée sur Streamlit](https://ocp7-froidure.streamlit.app/)

## Les données :

Les données sont issues du site Kagle [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)