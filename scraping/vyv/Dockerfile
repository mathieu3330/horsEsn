FROM python:3.9-slim

# Installer Chromium et Chromedriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir la variable d’environnement pour Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$PATH:/usr/bin/chromedriver"

# Copier les fichiers dans le conteneur
WORKDIR /app
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "vyvOffre.py"]
