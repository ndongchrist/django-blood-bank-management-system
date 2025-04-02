# Utiliser une image de base Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /django-blood-bank-management-system

# Copier les fichiers de requirements dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel l'application Django va tourner
EXPOSE 8000