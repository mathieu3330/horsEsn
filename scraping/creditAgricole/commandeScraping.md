### 🚀 **Adaptation du script pour Cloud Run Job**
Maintenant que ton script fonctionne en local, nous allons le **modifier pour être exécuté sur Cloud Run**.

---

## 🔹 **Modifications pour Cloud Run**
### **1️⃣ Remplacer l'adresse locale par Cloud SQL Socket**
Actuellement, ton script utilise :
```python
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}
```
Dans **Cloud Run**, on doit utiliser **la connexion Unix Socket** :
```python
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",  # Connexion Cloud SQL
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}
```

---

### **2️⃣ Optimiser l’Insertion dans la Base**
Actuellement, le script **peut insérer des doublons**.  
On ajoute **`ON CONFLICT DO NOTHING`** pour éviter cela :
```python
cursor.execute("""
    INSERT INTO offres (titre, contrat, lieu, lien, description)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (lien) DO NOTHING
""", (titre, contrat, lieu, lien, description))
```

---

### **3️⃣ Version Finale du Script (Compatible Cloud Run)**
```python
import os
import requests
import psycopg2
from bs4 import BeautifulSoup
import time

# 🔹 Connexion à Cloud SQL via Unix Socket
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",  # Cloud Run → Cloud SQL
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://jobs.totalenergies.com/fr_FR/careers/SearchJobs/?707=%5B42253%2C357336%2C42258%5D&707_format=1393&3834=%5B41588%5D&3834_format=3639&listFilterMode=1&jobRecordsPerPage=20&#jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def get_db_connection():
    """ Établit une connexion avec la base PostgreSQL """
    return psycopg2.connect(**DB_CONFIG)

def save_offer(titre, contrat, lieu, lien, description):
    """ Insère une offre en base de données (évite les doublons) """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (titre, contrat, lieu, lien, description)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (lien) DO NOTHING
        """, (titre, contrat, lieu, lien, description))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion dans la base : {e}")

def scrape_jobs():
    """ Scrape les offres et les enregistre en base """
    page = 0  
    while True:
        url = f"{BASE_URL}{page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Fin du scraping. Erreur HTTP.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="article article--result")

        if not offres:
            print(f"✅ Fin du scraping. Dernière page : {page // 20}")
            break

        print(f"📌 Scraping de la page {page // 20 + 1}... ({len(offres)} offres trouvées)")

        for offre in offres:
            try:
                titre_element = offre.find("h3", class_="article__header__text__title")
                titre = titre_element.text.strip() if titre_element else "Non précisé"
                lien = offre.find("a")["href"] if offre.find("a") else "Aucun lien"
                if lien.startswith("/"):
                    lien = "https://jobs.totalenergies.com" + lien

                contrat = offre.find("li", class_="list-item list-item-employmentType").text.strip() if offre.find("li", class_="list-item list-item-employmentType") else "Non précisé"
                lieu = offre.find("li", class_="list-item list-item-jobCountry").text.strip() if offre.find("li", class_="list-item list-item-jobCountry") else "Non précisé"

                description = "Non disponible"
                if lien != "Aucun lien":
                    time.sleep(1)
                    desc_response = requests.get(lien, headers=HEADERS)
                    if desc_response.status_code == 200:
                        desc_soup = BeautifulSoup(desc_response.text, "lxml")
                        desc_blocks = desc_soup.find_all("div", class_="article__content js_collapsible__content")
                        descriptions = [para.text.strip() for block in desc_blocks for para in block.find_all("p")]
                        if descriptions:
                            description = "\n".join(descriptions)

                save_offer(titre, contrat, lieu, lien, description)
            except Exception as e:
                print(f"⚠ Erreur lors du scraping : {e}")

        page += 20  

if __name__ == "__main__":
    scrape_jobs()
```

---

## 🚀 **Déploiement du Script sur Cloud Run Job**
### **1️⃣ Créer le Dockerfile**
Ajoute un fichier **`Dockerfile`** :
```dockerfile
FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir requests psycopg2 bs4 lxml

CMD ["python", "offreTotalCR.py"]
```

---

### **2️⃣ Construire et Pousser l’Image Docker**
Exécute ces commandes pour **construire et envoyer l’image** sur Google Cloud :
```sh
gcloud builds submit --tag gcr.io/projetdbt-450020/scraper-job-credit-agrc
```

---

### **3️⃣ Créer et Configurer Cloud Run Job**
Crée un **Cloud Run Job** qui se connecte à Cloud SQL :
```sh
gcloud run jobs create scraper-job-credit-agrc \
    --image=gcr.io/projetdbt-450020/scraper-job-credit-agrc \
    --region=us-central1 \
    --task-timeout=1800s \
    --max-retries=3 \
    --set-cloudsql-instances=projetdbt-450020:us-central1:projetcdinterne \
    --set-env-vars DB_HOST="/cloudsql/projetdbt-450020:us-central1:projetcdinterne",DB_NAME="postgres",DB_USER="postgres",DB_PASSWORD="root"
```

---

### **4️⃣ Tester le Job Cloud Run**
Lance **manuellement le job** pour voir s’il fonctionne :
```sh
gcloud run jobs execute scraper-job-credit-agrc --region=us-central1
```

---

### **5️⃣ Automatiser avec Cloud Scheduler**
Crée une **tâche automatique** pour exécuter le job chaque nuit à **2h du matin** :
```sh
gcloud scheduler jobs create http scraper-schedule \
    --schedule="0 2 * * *" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/projetdbt-450020/jobs/scraper-job:run" \
    --http-method=POST \
    --oauth-service-account-email=dbt-bigquery-service-account@projetdbt-450020.iam.gserviceaccount.com \
    --location=us-central1
```

---

## 🎯 **Résultat Final**
✅ **Scraping des offres TotalEnergies**  
✅ **Stockage dans Cloud SQL**  
✅ **Déploiement sur Cloud Run Job**  
✅ **Exécution automatique chaque nuit avec Cloud Scheduler**  

🔥 **Essaie cette version et dis-moi si ça fonctionne !** 🚀

---

### **🎯pour lancer en local**

cloud_sql_proxy -instances=projetdbt-450020:us-central1:projetcdinterne=tcp:5433

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

### **🎯 Résultat Final**
Ton script tourne **tous les jours à 2h du matin**, scrape les offres d'emploi et les stocke dans **Cloud SQL**, le tout **sans utiliser de variables d'environnement**. 🚀