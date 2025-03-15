![Entete](images/projet.png)

# 📌 Conception d’un Dashboard de Credit Scoring

## 📖 Contexte
**Prêt à Dépenser** est une société financière spécialisée dans le **crédit à la consommation**. Après avoir développé un **modèle de scoring crédit**, l’entreprise souhaite maintenant améliorer la **transparence des décisions** en mettant à disposition un **dashboard interactif** pour les chargés de relation client.

L’objectif est d’aider les chargés de relation client à **expliquer aux clients le score attribué** et à **comparer leurs caractéristiques avec d’autres profils similaires**.

## 🎯 Objectifs du Projet
- ✅ Développer un **dashboard interactif** accessible aux chargés de relation client.
- ✅ Visualiser le **score de crédit et sa probabilité** de manière intelligible.
- ✅ Comparer les caractéristiques d’un client avec d’autres profils similaires.
- ✅ Prendre en compte l’**accessibilité** pour les personnes en situation de handicap.
- ✅ Déployer le **dashboard sur le Cloud** pour qu’il soit accessible aux utilisateurs.

## 🛠️ Étapes du Projet

### 1️⃣ **Planification et Maquettage**
- Comprendre les **besoins des utilisateurs**.
- Concevoir des **maquettes simples** avant l’implémentation.
- Choix de la **technologie** Streamlit**.

### 2️⃣ **Développement du Dashboard**
- **Connexion à l’API de scoring** pour récupérer le score et la classe prédite.
- Implémenter des **visualisations claires et accessibles** :
  - Jauge colorée du **score de crédit**.
  - **Importance des features** ayant influencé la décision.
  - **Comparaison** avec l’ensemble des clients ou un groupe de clients similaires.
  - Analyse bi-variée entre **deux features sélectionnées**.
- Respecter les **critères d’accessibilité du WCAG**.

### 3️⃣ **Déploiement et Tests**
- Héberger le dashboard sur **une plateforme Cloud**.
- Tester l’interface avec des **utilisateurs finaux**.
- Optimiser l’expérience utilisateur (UX) et la navigation.

## 📦 Livrables Attendus
- ✅ Un **dashboard interactif fonctionnel**.
- ✅ Une **API intégrée** pour récupérer les scores en temps réel.
- ✅ Un **déploiement Cloud** accessible aux utilisateurs.
- ✅ Un **rapport décrivant l’implémentation et les choix technologiques**.
- ✅ Une **interface accessible** respectant les normes d’accessibilité.

## 🚀 Objectif Final
Offrir un **dashboard ergonomique et intuitif** permettant aux chargés de relation client d’**expliquer de manière transparente les décisions de crédit**, tout en permettant une **analyse comparative et une interaction fluide avec les données clients**.

## Descriptif de la structure :

repertoire			| description
------------------- | -----------
.github/workflows 	| Le Workflow github qui vient lancer les tests unitaires à chaque push du projet
Api 				| Le code de l'Api qui est déployée automatiquement vers Render lors d'un push
Appli				| L'application frontend déployée automatiquement vers Streamlit
tests				| Les tests unitaires réalisés avec Pytest

## Les liens vers l'application :

- [Application hébergée sur Streamlit](https://ocp8-froidure.streamlit.app/)
- [Dashboard Render](https://dashboard.render.com/)
- [API hébergée sur Render](https://ocp7-api.onrender.com/)
- [Test de l'API hébergée sur Render](https://ocp7-api.onrender.com/docs/)

---
- 👥 **Compétences requises** : Python, Data Visualization, API, Streamlit.
- 📅 **Technologies** : Streamlit, Cloud Deployment, Sklearn, Pandas.
- 🌍 **Source des données** : Issues du site Kagle [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)
