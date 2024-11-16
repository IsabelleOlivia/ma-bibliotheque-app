
# Bibliothèque App

## Description
Une application Flask pour gérer une bibliothèque avec des fonctionnalités d'emprunt et de retour de livres, orchestrée avec Docker.

## Structure du projet
- **app.py** : Code principal de l'application Flask.
- **templates/** : Contient les fichiers HTML.
- **data/** : Contient le fichier PostgresSql pour les données.
- **Dockerfile** : Définit l'image Docker de l'application.
- **docker-compose.yml** : Orchestre les services `app` et `db`.