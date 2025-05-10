import requests
import psycopg2
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

LOGO_INFORMATIQUECDC = "https://pbs.twimg.com/profile_images/1144283551975858177/mLPOllEo_400x400.jpg"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

BASE_URL = "https://informatiquecdc-career.talent-soft.com/offre-de-emploi/liste-offres.aspx?page={}&LCID=1036"
BASE_DETAIL_URL = "https://informatiquecdc-career.talent-soft.com/offre-de-emploi/{}"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour analyser le contenu HTML
def parse_html_content(raw_html):
    return BeautifulSoup(raw_html, "lxml").get_text(separator="\n", strip=True)

# Fonction pour récupérer la description complète de l'offre
def get_description(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible", "Non précisé"

        soup = BeautifulSoup(response.text, "html.parser")

        # Description de la mission
        description_section = soup.find("div", id="fldjobdescription_description1")
        description = parse_html_content(str(description_section)) if description_section else "Description non disponible"

        # Contrat
        contrat_section = soup.find("p", id="fldjobdescription_contract")
        contrat = contrat_section.get_text(strip=True) if contrat_section else "Non précisé"

        return description, contrat

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible", "Non précisé"

# Fonction pour vérifier si l'offre existe déjà dans la base de données
def offer_exists(titre, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM offres WHERE titre = %s AND description = %s AND nomclient = 'informatiqueCDC'
        """, (titre, description))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"⚠ Erreur vérification existence offre : {e}")
        return False

# Fonction pour enregistrer les offres dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
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
            "informatiqueCDC", LOGO_INFORMATIQUECDC, "prive", "non précisé", date_publication
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_informatiquecdc():
    page = 1
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("div", class_="ts-offer-card")

        if not job_list_items:
            print("✅ Aucune offre trouvée.")
            break

        for job_item in job_list_items:
            try:
                titre = job_item.find("h3").get_text(strip=True)
                lien = "https://informatiquecdc-career.talent-soft.com" + job_item.find("a")["href"]
                ville = job_item.find("li", class_="noBorder").get_text(strip=True)
                lieu = "France"
                date_pub = job_item.find("li").find_next("li").get_text(strip=True)
                date_pub = datetime.strptime(date_pub, "%d/%m/%Y").date()

                description, contrat = get_description(lien)

                if offer_exists(titre, description):
                    print(f"✅ Offre déjà existante : {titre} ({ville})")
                    continue  # Passe à l'offre suivante si elle existe déjà

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub)
                print(f"✅ Offre enregistrée : {titre} ({ville})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_informatiquecdc()
