# Utiliser une image Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY hermesOffre.py requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande d'exécution du script
CMD ["python", "hermesOffre.py"]
