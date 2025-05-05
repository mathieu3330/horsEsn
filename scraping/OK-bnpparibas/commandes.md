
### **2️⃣ Construire et Pousser l’Image Docker**
Exécute ces commandes pour **construire et envoyer l’image** sur Google Cloud :
```sh
gcloud builds submit --tag gcr.io/projetdbt-450020/scraper-job-bnpparibas

```

---

### **3️⃣ Créer et Configurer Cloud Run Job**
Crée un **Cloud Run Job** qui se connecte à Cloud SQL :
```sh
gcloud run jobs create scraper-job-bnpparibas \
    --image=gcr.io/projetdbt-450020/scraper-job-bnpparibas \
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
