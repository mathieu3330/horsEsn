# Utiliser une image Python légère
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir fastapi psycopg2 uvicorn

# Exposer le port 8080
EXPOSE 8080

# Lancer l'API avec Uvicorn
CMD ["uvicorn", "offreApi:app", "--host", "0.0.0.0", "--port", "8080"]
