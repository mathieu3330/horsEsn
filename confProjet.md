
1. Lister les comptes actuellement configurés
gcloud auth list

3. Te connecter avec le nouveau compte
gcloud auth login


4. Vérifier que le bon compte est maintenant actif
gcloud config list account
ou
gcloud auth list

5. (Optionnel) Définir ce compte comme actif (si plusieurs sont connectés)

gcloud config set account NOUVEAU_EMAIL@gmail.com


Dans ton cas, si l’ID du projet est horsesn, exécute :

gcloud config set project horsesn

✅ 4. Activer les services pour le nouveau projet
Si ce projet est tout nouveau, active les APIs nécessaires :

gcloud services enable run.googleapis.com cloudbuild.googleapis.com sqladmin.googleapis.com artifactregistry.googleapis.com


✅ 5. Redéployer dans le bon projet
Maintenant tu peux reconstruire et déployer dans Cloud Run avec ton nouveau projet :

bash
Copier
Modifier
gcloud builds submit --tag gcr.io/horsesn/scraper-job-vyv

gcloud run jobs create scraper-job-vyv \
    --image=gcr.io/horsesn/scraper-job-vyv \
    --region=us-central1 \
    --task-timeout=1800s \
    --max-retries=3 \
    --set-cloudsql-instances=horsesn:us-central1:projetcdinterne \
    --set-env-vars DB_HOST="/cloudsql/horsesn:us-central1:projetcdinterne",DB_NAME="postgres",DB_USER="postgres",DB_PASSWORD="root"
Remplace bien tous les anciens ID (projetdbt-450020) par horsesn.



✅ Étapes à suivre :
1. Va dans la console IAM :
👉 https://console.cloud.google.com/iam-admin/iam

2. Sélectionne ton projet horsesn.
3. Vérifie que l'adresse horsesn.fr@gmail.com est bien ajoutée comme membre du projet.
4. Si ce n’est pas le cas, ajoute-la avec ces rôles minimums :
Cloud Build Editor (ou Editor pour tout faire)

Storage Admin (pour gs:// accès)

Artifact Registry Administrator (si tu l'utilises)


