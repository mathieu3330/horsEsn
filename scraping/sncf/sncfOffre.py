import requests
import psycopg2
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://sncf-preprod.talentry.com/api/v1/tenants/1561/jobs/list?sort=lastChangeDate&desc=1&page={}&radius=5&tagData%5B187%5D=2230%2C2229%2C2228%2C2231&pageSize=20&offset=40"
DESCRIPTION_URL = "https://emploi.sncf.com/nos-offres/{}"  # URL de la page de l'offre pour la description

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

LOGO_SNCF = "https://sncf-preprod.talentry.com/image/bupka5pjg3sd2hy76u3vxg"  # URL du logo de l'entreprise

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer la description complète de l'offre
def get_description_details(offer_id):
    try:
        # Accéder à la page détaillée de l'offre via l'ID de l'offre
        response = requests.get(DESCRIPTION_URL.format(offer_id), headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        # Recherche de la section contenant la description
        description_section = soup.find("div", class_="prose")

        if description_section:
            description = description_section.get_text(separator="\n", strip=True)
            return description
        return "Description non disponible"
    
    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

# Fonction pour récupérer la date de publication de l'offre
def get_offer_date(creation_date):
    try:
        date_obj = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S+00:00").date()
        return date_obj
    except Exception as e:
        print(f"⚠ Erreur récupération date de l'offre : {e}")
        return datetime.today().date()

# Fonction pour vérifier si l'offre existe déjà dans la base de données
def offer_exists(titre, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM offres WHERE titre = %s AND description = %s AND nomclient = 'sncf'
        """, (titre, description))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"⚠ Erreur vérification existence offre : {e}")
        return False

# Fonction pour enregistrer les offres dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, teletravail, date_publication):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, 
                nomclient, logo, secteur, teletravail, dateoffre
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, 
            "sncf", LOGO_SNCF, "public", teletravail, date_publication
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_sncf():
    page = 1
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        try:
            # Charger la réponse JSON
            data = response.json()
            job_list = data.get("list", [])

            if not job_list:
                print("✅ Aucune offre trouvée.")
                break

            for job_item in job_list:
                try:
                    titre = job_item["translations"]["fr"]["name"]
                    
                    # Récupérer le contrat directement à partir de "tagValues"
                    contrat = None
                    for tag in job_item.get("tagValues", []):
                        if "CDI" in tag["translations"]["fr"]["name"]:
                            contrat = "CDI"
                        elif "CDD" in tag["translations"]["fr"]["name"]:
                            contrat = "CDD"
                        elif "ALTERNANCE" in tag["translations"]["fr"]["name"]:
                            contrat = "Alternance"
                        elif "STAGE" in tag["translations"]["fr"]["name"]:
                            contrat = "Stage"
                        if contrat:
                            break
                    
                    # Si le contrat n'est pas trouvé, par défaut, attribuer "Autre"
                    if not contrat:
                        contrat = "non précisé"
                    
                    location = job_item["locations"][0]["translations"]["fr"]["name"]
                    city = location.split(",")[0].strip()

                    lien = f"https://emploi.sncf.com/nos-offres/{job_item['newId']}"
                    description = get_description_details(job_item["id"])  # Récupérer la description détaillée
                    telework = "non précisé"  # Assuming all jobs are on-site, adjust as needed
                    date_posted = get_offer_date(job_item["creationDate"])

                    if offer_exists(titre, description):
                        print(f"✅ Offre déjà existante : {titre} ({city})")
                        stop_scraping = True  # Arrêter le scraping dès qu'une offre existe déjà
                        break  # Sortir de la boucle

                    save_offer(titre, contrat, "France", city, lien, description, telework, date_posted)
                    print(f"✅ Offre enregistrée : {titre} ({city})")

                except Exception as e:
                    print(f"⚠ Erreur traitement offre : {e}")

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur parsing JSON : {e}")
            break

if __name__ == "__main__":
    scrape_sncf()
