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

BASE_URL = "https://joinus.saint-gobain.com/fr?f%5B0%5D=country%3Afr&f%5B1%5D=type_contrat%3A36&f%5B2%5D=type_contrat%3A38&f%5B3%5D=type_contrat%3A39&f%5B4%5D=type_contrat%3A41&page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers",
    "Origin": "https://joinus.saint-gobain.com",
    "Referer": "https://joinus.saint-gobain.com/fr?f%5B0%5D=country%3Afr&f%5B1%5D=type_contrat%3A36&f%5B2%5D=type_contrat%3A38&f%5B3%5D=type_contrat%3A39&f%5B4%5D=type_contrat%3A41&page=1"
}

LOGO_SAINT_GOBLAIN = "https://www.saint-gobain.com/sites/default/files/styles/logo_full/public/2020-07/saint-gobain_logo_rgb_fr.svg"

# Création de la session pour maintenir les cookies
session = requests.Session()
session.headers.update(HEADERS)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'saint-gobain'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_html_content(raw_html):
    return BeautifulSoup(raw_html, "lxml").get_text(separator="\n", strip=True)

def get_offer_details(url):
    try:
        response = session.get(url)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code} pour l'URL {url}")
            return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date(), "Non précisé"

        soup = BeautifulSoup(response.text, "html.parser")

        # Description de l'offre
        description_section = soup.find("div", class_="offre-edito")
        description = description_section.get_text(strip=True) if description_section else "Description non disponible"

        # Ville de l'offre
        city = soup.find("p", id="fldlocation_location_geographicalareacollection")
        city = city.get_text(strip=True) if city else "Non précisé"

        # Contrat (Alternance, CDI, CDD, etc.)
        contrat_section = soup.find("p", id="fldjobdescription_contract")
        contrat = contrat_section.get_text(strip=True) if contrat_section else "Non précisé"

        # Salaire
        salaire_section = soup.find("div", class_="field__item")
        salaire = "Non précisé"
        if salaire_section:
            salary = salaire_section.find("span", class_="field__item")
            if salary:
                salaire = salary.get_text(strip=True).replace("\xa0", " ").replace("par mois", "").strip()

        # Date de publication
        posted_timestamp = soup.find("div", class_="date")
        posted_date = posted_timestamp.find("span", class_="value").get_text() if posted_timestamp else ""
        try:
            date_pub = datetime.strptime(posted_date, "%d/%m/%Y").date() if posted_date else datetime.min.date()
        except Exception as e:
            date_pub = datetime.min.date()

        return description, contrat, city, date_pub, salaire

    except Exception as e:
        print(f"⚠ Erreur récupération détails de l'offre : {e}")
        return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date(), "Non précisé"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, salaire):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, salaire
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            "saint-gobain", LOGO_SAINT_GOBLAIN, "prive", salaire
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_saint_gobain():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = session.get(url)

        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code}. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("div", class_="offer-card-body")

        if not job_list_items:
            print("✅ Aucune offre trouvée.")
            break

        for job_item in job_list_items:
            try:
                titre_el = job_item.find("a", class_="title--cta")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"

                lien = f"https://joinus.saint-gobain.com{job_item.find('a')['href']}" if job_item.find('a') else None

                description, contrat, ville, date_posted, salaire = get_offer_details(lien)

                if date_posted <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                save_offer(titre, contrat, "France", ville, lien, description, date_posted, salaire)
                print(f"✅ Offre enregistrée : {titre} ({ville})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_saint_gobain()
