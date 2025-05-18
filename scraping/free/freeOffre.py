import requests
import psycopg2
from datetime import datetime
import time
from bs4 import BeautifulSoup

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

LOGO_FREE = "https://www.affinicia.com/forfait-mobile/wp-content/uploads/sites/3/2021/06/free-logo.png"

BASE_URL = "https://recrutement.iliad-free.fr/offres/{}?localisation=%22%22"
DETAILS_URL = "https://recrutement.iliad-free.fr/offre/{}"  # URL détaillée de l'offre

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Récupérer la dernière date d'offre enregistrée
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'free'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print(f"❌ Erreur récupération date : {e}")
        return datetime.min.date()

# Fonction pour analyser le contenu HTML
def parse_html_content(raw_html):
    return BeautifulSoup(raw_html, "lxml").get_text(separator="\n", strip=True)

# Fonction pour obtenir les détails de l'offre
def get_offer_details(url):
    print(f"📄 ======= get_offer_details  ===> {url}")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Description non disponible", "Non précisé", "Non précisé", "Non précisé", datetime.min.date()

        soup = BeautifulSoup(response.text, "html.parser")

        # Description
        description_section = soup.find("div", class_="card-body")
        description = description_section.get_text(strip=True) if description_section else "Description non disponible"
        print(f"📄 fin description  ===> {description}")

        # Localisation
        location_section = soup.find("div", class_="localisations")
        city = location_section.get_text(strip=True) if location_section else "Non précisé"
        print(f"📄 ======= city  ===> {city}")

        return description, city

    except Exception as e:
        print(f"⚠ Erreur récupération détails de l'offre : {e}")
        return "Description non disponible", "Non précisé"

# Fonction pour enregistrer une offre dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, salaire, date_publication):
    print(f"📄 ======= save  =======")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, salaire, dateoffre,
                nomclient, logo, secteur
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, salaire, date_publication,
            "free", LOGO_FREE, "public"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_free():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("a", class_="card")

        if not job_list_items:
            print("✅ Aucune offre trouvée.")
            break

        for job_item in job_list_items:
            try:
                titre = job_item.find("h2", class_="title").get_text(strip=True)
                print(f"📄 titre ===> {titre}")

                # Vérification si le lien existe avant de l'utiliser
                lien = job_item["href"] if "href" in job_item.attrs else None
                print(f"📄 fin lien  ===> {lien}")
                
                if lien:
                    lien = f"https://recrutement.iliad-free.fr{lien}"
                else:
                    print(f"❌ Lien non trouvé pour l'offre : {titre}")
                    continue  # Passer à l'offre suivante si le lien est manquant

                # Récupérer les autres informations comme le contrat, la date de publication directement sur la page des offres
                contrat_section = job_item.find("div", class_="card-tags")
                contrat = "Non précisé"
                if contrat_section:
                    contrat_list = contrat_section.find_all("li")
                    for item in contrat_list:
                        if "CDD" in item.get_text() or "CDI" in item.get_text() or "STAGE" in item.get_text() or "ALTERNANCE" in item.get_text():
                            contrat = item.get_text().strip()
                print(f"📄 contrat ===> {contrat}")

                # Récupérer la date de publication
                posted_date_section = job_item.find("p", class_="time")
                posted_date = posted_date_section.get_text(strip=True) if posted_date_section else "Non précisé"
                print(f"📄 posted_date_section ===> {posted_date}")
                
                date_pub = datetime.min.date()
                if "Mise en ligne le" in posted_date:
                    date_part = posted_date.split("Mise en ligne le")[-1].strip()
                    try:
                        date_pub = datetime.strptime(date_part, "%d/%m/%Y").date()  # Convertir en date
                    except ValueError:
                        date_pub = datetime.min.date()
                print(f"📄 date_pub ===> {date_pub}")

                description, city = get_offer_details(lien)

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                save_offer(titre, contrat, "France", city, lien, description, "Non précisé", date_pub)
                print(f"✅ Offre enregistrée : {titre} ({city})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_free()
