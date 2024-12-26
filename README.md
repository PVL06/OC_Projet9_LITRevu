# OC Projet 9: LITRevu
Présentation du projet

Ce projet s’inscrit dans le cadre du parcours "Développeur d’application Python" sur OpenClassrooms. Il consiste à développer une application web permettant la publication et la consultation de critiques de livres et d’articles.

Fonctionnalités principales:

* Authentification sécurisée : gestion de l’inscription et de la connexion des utilisateurs.
* Publication de critiques : les utilisateurs peuvent partager leurs avis détaillés sur des livres ou articles qu’ils ont lus.
* Demande de critiques : possibilité de solliciter l’opinion d’autres lecteurs sur des œuvres spécifiques.
* Gestion des publications : modification et suppression des critiques publiées.
* Suivi d’autres utilisateurs : suivre d’autres membres pour consulter leurs demandes et publications de critiques.
* Interface d'administration : gestion des utilisateurs, des tickets et des critiques

L'objectif pédagogique de ce projet a pour but de prendre en main le framework Django et de manipuler une base de données SQLite.


## Installation

1. Cloner le dépôt
```
git clone https://github.com/PVL06/OC_Projet9_LITRevu.git
```

2. Créer et activer un environnement virtuel Python (venv)

```
cd OC_Projet9_LIRevuT
python -m venv env
```
Activation de l'environnement virtuel sur Windows
```
env\Scripts\activate
```
Activation de l'environnement virtuel sur macOS et Linux
```
source env/bin/activate
```
3. Installer des dépendances
Utilisez pip pour installer les bibliothèques nécessaires
```
pip install -r requirements.txt
```

## Lancement du serveur

1. Initialiser la base de donnée
```
cd LITRevu
python manage.py migrate
```

2. Lancer le serveur
```
python manage.py runserver
```

3. Accès au site
Se rendre sur un navigateur a l'adresse https://localhost:8000/ ou https://127.0.0.1:8000/
