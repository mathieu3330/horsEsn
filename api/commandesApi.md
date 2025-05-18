
```sh
gcloud auth login
gcloud config set project horsesn
```

### **2️⃣ Construire l’image Docker**
Exécute cette commande **dans le dossier contenant `offreApi.py` et `Dockerfile`** :

```sh
gcloud builds submit --tag gcr.io/horsesn/api-offres
```

✅ **L’image est maintenant stockée dans Google Artifact Registry.**

---

## ✅ **4️⃣ Déployer sur Cloud Run**
### **Vérifier que Cloud Run a accès à Cloud SQL**
Cloud Run doit **avoir les permissions pour accéder à Cloud SQL**.

1️⃣ **Ajouter le rôle `cloudsql.client` à Cloud Run :**
```sh
gcloud projects add-iam-policy-binding horsesn \
    --member=serviceAccount:your-service-account@horsesn.iam.gserviceaccount.com \
    --role=roles/cloudsql.client
```

2️⃣ **Vérifier si Cloud SQL est bien accessible :**
```sh
gcloud sql instances describe offres --format="value(settings.ipConfiguration)"
```
Si **IP publique activée**, alors assure-toi que **Cloud Run est autorisé dans les réseaux**.

---

### **Déployer le Service Cloud Run**
Exécute cette commande pour **déployer l'API sur Cloud Run** :

```sh
gcloud run deploy api-offres \
    --image=gcr.io/horsesn/api-offres \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --add-cloudsql-instances=horsesn:us-central1:offres \
    --set-env-vars DB_HOST="/cloudsql/horsesn:us-central1:offres",DB_NAME="postgres",DB_USER="postgres",DB_PASSWORD="root" \
    --port=8080
```

📌 **Explication des options :**
- `--allow-unauthenticated` → Rend l'API accessible publiquement.
- `--add-cloudsql-instances=horsesn:us-central1:offres` → Connexion à Cloud SQL.
- `--set-env-vars` → Définit les paramètres de connexion à PostgreSQL.

✅ **Une URL sera générée pour ton API**, par exemple :
```
https://api-offres-xxxxx.a.run.app
```

---

## ✅ **5️⃣ Tester l’API Déployée**
### **Tester l’API avec `curl` :**
```sh
curl https://api-offres-515518215606.us-central1.run.app
```
💡 **Doit afficher :**  
```json
{"message": "API de gestion des offres d'emploi"}
```

### **Lister toutes les offres :**
```sh
curl https://api-offres-xxxxx.a.run.app/offres
```

### **Filtrer les offres (Ex: CDI à Paris) :**
```sh
curl "curl https://api-offres-515518215606.us-central1.run.app/offres?contrat=CDI&lieu=Paris"
```

---

## ✅ **6️⃣ Vérifier les Logs en Cas d’Erreur**
Si l’API ne fonctionne pas, vérifie les logs avec cette commande :
```sh
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=api-offres" --limit 50 --format json
```
Ou va directement voir les logs dans **Google Cloud Console** ici :  
🔗 [Cloud Run Logs](https://console.cloud.google.com/logs/viewer?project=horsesn&resource=cloud_run_revision)

---

## 🎯 **Résumé du Déploiement**
| 📌 **Étape** | ✅ **Action** |
|-------------|------------------|
| **1️⃣ Préparer FastAPI** | Ajout de `--host 0.0.0.0 --port 8080` |
| **2️⃣ Créer un Dockerfile** | Exposer le bon port et installer les dépendances |
| **3️⃣ Construire l’image Docker** | `gcloud builds submit --tag gcr.io/horsesn/api-offres` |
| **4️⃣ Déployer sur Cloud Run** | `gcloud run deploy api-offres ...` |
| **5️⃣ Tester l’API déployée** | `curl https://api-offres-xxxxx.a.run.app/` |
| **6️⃣ Vérifier les logs** | `gcloud logging read` |

🚀 **Ton API est maintenant en ligne sur Cloud Run et connectée à Cloud SQL !**  
Tu veux ajouter des **authentifications JWT** ou **un frontend React** pour l’afficher ? 😊



=================================== Full text search =============================

Ajout d'un index Full-Text Search (FTS) sur titre et description (tu devras l’exécuter dans PostgreSQL) :

CREATE INDEX idx_offres_fts ON "public"."offres" USING GIN (to_tsvector('french', titre || ' ' || description));


Script: 

import os
from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# 🔹 Connexion à Cloud SQL via Cloud Run
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_db_connection():
    """ Établit une connexion PostgreSQL """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.get("/")
def read_root():
    return {"message": "API de gestion des offres d'emploi"}

@app.get("/offres")
def get_offres(contrat: str = Query(None), lieu: str = Query(None), search: str = Query(None)):
    """ Récupère toutes les offres avec filtres facultatifs et recherche Full-Text """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM offres 
        WHERE 1=1
    """
    params = []

    if contrat:
        query += " AND contrat = %s"
        params.append(contrat)
    if lieu:
        query += " AND lieu = %s"
        params.append(lieu)
    if search:
        query += " AND to_tsvector('french', titre || ' ' || description) @@ plainto_tsquery('french', %s)"
        params.append(search)

    query += " ORDER BY date_scraping DESC"  # Trier par date la plus récente

    cursor.execute(query, tuple(params))
    offres = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return {"offres": offres}

@app.get("/offres/{offre_id}")
def get_offre(offre_id: int):
    """ Récupère une offre spécifique par son ID """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM offres WHERE id = %s", (offre_id,))
    offre = cursor.fetchone()

    cursor.close()
    conn.close()

    if not offre:
        return {"message": "Offre non trouvée"}

    return offre

# 🔹 Démarrer l'API pour Cloud Run (Uvicorn)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Cloud Run fournit ce port dynamiquement
    uvicorn.run(app, host="0.0.0.0", port=port)
