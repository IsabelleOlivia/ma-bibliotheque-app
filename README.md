# Bibliothèque App

## Description
L'application **Bibliothèque App** est une application Flask qui permet de gérer une bibliothèque (emprunt, retour, etc.). Elle est orchestrée avec Docker pour assurer une exécution fluide des différents composants, notamment une base de données PostgreSQL.

---

## Structure du projet

```
Bibliothèque/
│
├── app.py                  # Code principal de l'application Flask
├── templates/              # Contient les fichiers HTML (interface utilisateur)
├── data/                   # Répertoire pour persister les données PostgreSQL
├── requirements.txt        # Liste des dépendances Python
├── Dockerfile              # Définition de l'image Docker de l'application
├── docker-compose.yml      # Orchestration des services avec Docker Compose
└── README.md               # Documentation
```

---

## Prérequis
Avant de lancer le projet, assurez-vous d'avoir installé les outils suivants :
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Instructions d'exécution

### 1. Créer le réseau Docker
Un réseau personnalisé est nécessaire pour permettre la communication entre l'application Flask et la base de données PostgreSQL.

```bash
docker network create mynetwork
```

---

### 2. Lancer la base de données PostgreSQL

Démarrez le conteneur PostgreSQL avec la commande suivante. Les données seront persistées dans le répertoire `./data`.

```bash
docker run -d --name postgres_db --network mynetwork \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=bibliotheque \
  -v ./data:/var/lib/postgresql/data \
  postgres:latest
```

---

### 3. Lancer l'application Flask

Utilisez l'image Docker publiée sur Docker Hub pour démarrer l'application Flask. Veillez à fournir la bonne URL de connexion à la base de données.

```bash
docker run -d --name Ma_bibliotheque --network mynetwork \
  -e DATABASE_URL=postgresql://user:password@postgres_db:5432/bibliotheque \
  -p 5000:5000 \
  isaolivia/ma_bibliotheque:latest
```

---

### 4. Accéder à l'application

Une fois les conteneurs démarrés, accédez à l'application via votre navigateur :
- **URL** : [http://localhost:5000](http://localhost:5000)

---



### 2. Base de données inaccessible
Si l'application Flask ne peut pas se connecter à la base de données, assurez-vous que les variables d'environnement `POSTGRES_USER`, `POSTGRES_PASSWORD`, et `POSTGRES_DB` correspondent à celles utilisées dans l'URL de connexion (`DATABASE_URL`).


Avec ces instructions, vous devriez être capable de lancer et de gérer l'application **Bibliothèque App** avec Docker. 🎉