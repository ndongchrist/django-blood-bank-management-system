###  configuration de Dockerfile et Docker Compose pour une application Django avec une base de données postgresSql

#### Introduction

Dans ce cours, nous allons apprendre à configurer un environnement de développement pour une application Django en utilisant Docker. Nous allons créer un `Dockerfile` pour définir l'environnement de notre application Django et un fichier `docker-compose.yml` pour orchestrer les services de notre application, y compris la base de données.


#### Étape 1: Structure du projet

Supposons que vous avez une structure de projet Django comme suit :

```
my_django_app/
│
├── my_django_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── ...
```

#### Étape 2: Création du Dockerfile

Le `Dockerfile` est un script qui contient une série d'instructions pour créer une image Docker. Cette image sera utilisée pour exécuter notre application Django.

1. **Créer un fichier `Dockerfile` à la racine du projet** :

   ```Dockerfile
   # Utiliser une image de base Python
   FROM python:3.9-slim

   # Définir le répertoire de travail dans le conteneur
   WORKDIR /app

   # Copier les fichiers de requirements dans le conteneur
   COPY requirements.txt /app/

   # Installer les dépendances
   RUN pip install --no-cache-dir -r requirements.txt

   # Copier le reste du code de l'application
   COPY . /app/

   # Exposer le port sur lequel l'application Django va tourner
   EXPOSE 8000

   # Commande pour exécuter l'application
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

2. **Explication des instructions** :

   - `FROM python:3.9-slim` : Utilise une image de base Python 3.9.
   - `WORKDIR /app` : Définit le répertoire de travail dans le conteneur.
   - `COPY requirements.txt /app/` : Copie le fichier `requirements.txt` dans le conteneur.
   - `RUN pip install --no-cache-dir -r requirements.txt` : Installe les dépendances Python listées dans `requirements.txt`.
   - `COPY . /app/` : Copie tout le code de l'application dans le conteneur.
   - `EXPOSE 8000` : Expose le port 8000 pour que l'application Django puisse être accessible.
   - `CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]` : Commande par défaut pour exécuter le serveur de développement Django.

#### Étape 3: Création du fichier docker-compose.yml

Le fichier `docker-compose.yml` permet de définir et de gérer plusieurs conteneurs Docker. Dans notre cas, nous allons définir deux services : un pour l'application Django et un autre pour la base de données PostgreSQL.

1. **Créer un fichier `docker-compose.yml` à la racine du projet** :

   ```yaml
   version: '3.8'

   services:
     db:
       image: postgres:13
       environment:
         POSTGRES_DB: my_django_db
         POSTGRES_USER: my_django_user
         POSTGRES_PASSWORD: my_django_password
       volumes:
         - postgres_data:/var/lib/postgresql/data/

     web:
       build: .
       command: python manage.py runserver 0.0.0.0:8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         - DATABASE_URL=postgres://my_django_user:my_django_password@db:5432/my_django_db

   ```

2. **Explication des sections** :

   - **version** : Spécifie la version de Docker Compose.
   - **services** : Définit les services (conteneurs) à exécuter.
     - **db** : Service pour la base de données PostgreSQL.
       - `image: postgres:13` : Utilise l'image officielle de PostgreSQL version 13.
       - `environment` : Définit les variables d'environnement pour configurer la base de données.
       - `volumes` : Persiste les données de la base de données dans un volume Docker.
     - **web** : Service pour l'application Django.
       - `build: .` : Construit l'image Docker à partir du `Dockerfile` dans le répertoire courant.
       - `command` : Commande pour exécuter le serveur de développement Django.
       - `volumes` : Monte le répertoire courant dans le conteneur pour permettre des modifications en temps réel.
       - `ports` : Expose le port 8000 de l'application Django sur le port 8000 de l'hôte.
       - `depends_on` : Assure que le service `db` est démarré avant le service `web`.
       - `environment` : Définit les variables d'environnement pour configurer la connexion à la base de données.

   - **volumes** : Définit un volume nommé pour persister les données de la base de données.

#### Étape 4: Configuration de Django pour utiliser PostgreSQL

1. **Modifier `settings.py` pour utiliser PostgreSQL** :

   ```python
   

   DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

   ```

#### Étape 5: Exécution des conteneurs

1. **Construire et démarrer les conteneurs** :

   ```bash
   docker-compose up --build
   ```

   Cette commande va construire les images Docker et démarrer les conteneurs pour l'application Django et la base de données PostgreSQL.

2. **Accéder à l'application** :

   Une fois les conteneurs démarrés, vous pouvez accéder à l'application Django en ouvrant un navigateur et en allant à l'adresse `http://localhost:8000`.

#### Étape 6: Gestion des migrations

1. **Exécuter les migrations** :

   Si vous avez besoin d'exécuter les migrations de base de données, vous pouvez le faire en exécutant la commande suivante dans un autre terminal :

   ```bash
   docker-compose exec web python manage.py migrate
   ```

#### Étape 7: Arrêt des conteneurs

1. **Arrêter les conteneurs** :

   Pour arrêter les conteneurs, utilisez la commande suivante :

   ```bash
   docker-compose down
   ```

   Cela arrêtera et supprimera les conteneurs, mais conservera les volumes (comme les données de la base de données).

#### Conclusion

Dans ce cours, nous avons appris à configurer un environnement de développement pour une application Django en utilisant Docker. Nous avons créé un `Dockerfile` pour définir l'environnement de notre application et un fichier `docker-compose.yml` pour orchestrer les services de notre application, y compris la base de données PostgreSQL. Cette configuration permet de développer et de tester l'application de manière isolée et reproductible.

### Questions et exercices

1. **Question** : Pourquoi est-il important d'utiliser des volumes Docker pour la base de données ?
2. **Exercice** : Modifiez le fichier `docker-compose.yml` pour ajouter un service Redis et configurez Django pour utiliser Redis comme cache.
3. **Exercice** : Ajoutez un service `nginx` pour servir l'application Django en production.

### Ressources supplémentaires

- [Documentation officielle de Docker](https://docs.docker.com/)
- [Documentation officielle de Docker Compose](https://docs.docker.com/compose/)
- [Documentation officielle de Django](https://docs.djangoproject.com/)

Ce cours vous fournit une base solide pour configurer et gérer des applications Django avec Docker. Avec ces connaissances, vous pouvez maintenant expliquer et enseigner cette configuration à d'autres développeurs.