# Utiliser une image Python officielle
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY bnpparibasOffre.py requirements.txt ./

# Installer les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Commande d'exécution du script Python
CMD ["python", "bnpparibasOffre.py"]
