import requests
import psycopg2
from datetime import datetime
import time
import html
from bs4 import BeautifulSoup

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

# URL de base pour Eiffage avec pagination
BASE_URL = "https://jobs.eiffage.com/fr/sites/eiffage-carriere/home/toutes-nos-offres/area-content/recherchez-le-poste-qu-il-vous-f.xhtml?returnFilters=false&page={}&query=&country=France"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

LOGO_EIFFAGE = "https://download.logo.wine/logo/Eiffage/Eiffage-Logo.wine.png"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Nouvelle méthode pour vérifier si l'offre existe déjà dans la base de données (par titre + description)
def check_offer_exists(titre, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM offres WHERE titre = %s AND description = %s
        """, (titre, description))
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result > 0
    except Exception as e:
        print(f"⚠ Erreur vérification doublon : {e}")
        return False

# Fonction pour récupérer la description détaillée de l'offre
def get_description_details(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        description_section = soup.find("div", class_="offer-detail__left-sections-container")

        if description_section:
            description = description_section.get_text(separator="\n", strip=True)
            return description
        return "Description non disponible"

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

# Fonction pour récupérer le type de contrat à partir du titre
def get_contrat_from_title(titre):
    if "alternant" in titre.lower():
        return "Alternance"
    elif "stage" in titre.lower():
        return "Stage"
    elif "cdd" in titre.lower():
        return "CDD"
    else:
        return "CDI"

# Fonction pour enregistrer les offres dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, teletravail, nomclient, logo, groupeparent):
    try:
        # Vérification de l'existence de l'offre avant d'insérer
        if check_offer_exists(titre, description):
            print(f"⚠ Offre déjà présente : {titre}")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail, groupeparent
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            nomclient, logo, "prive", teletravail, groupeparent
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Offre enregistrée : {titre} ({ville})")
    except Exception as e:
        print(f"⚠ Erreur insertion BDD : {e}")

# Fonction principale de scraping
def scrape_eiffage():
    page = 1
    stop_scraping = False
    today = datetime.now().date()  # Utiliser la date du jour
    
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
            job_list_items = data.get("hits", [])

            if not job_list_items:
                print("✅ Aucune offre trouvée.")
                break

            for job_item in job_list_items:
                try:
                    titre = job_item.get("title", "Non précisé")
                    contrat = job_item.get("jobType", "Non précisé")
                    location = job_item.get("city", "Non précisé")
                    lien = f"https://jobs.eiffage.com{job_item.get('url', '')}"
                    description = get_description_details(lien)  # Récupérer la description détaillée
                    date_posted = today  # Utiliser la date d'aujourd'hui
                    telework = "non précisé"  # Ajuster selon les informations de télétravail disponibles

                    if titre.strip() == "" or description.strip() == "":
                        print("⏹ Offre sans titre ou description, arrêt du scraping.")
                        stop_scraping = True
                        break

                    save_offer(titre, contrat, "France", location, lien, description, date_posted, telework, "Eiffage", LOGO_EIFFAGE, "Eiffage")

                except Exception as e:
                    print(f"⚠ Erreur traitement offre : {e}")

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur parsing JSON : {e}")
            break

if __name__ == "__main__":
    scrape_eiffage()
