import requests
import psycopg2
from datetime import datetime
import time
import html
from bs4 import BeautifulSoup

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://careers.societegenerale.com/rechercher?refinementList[jobLocation][0]=FRA&refinementList[jobType][0]=APPRENTICESHIP&refinementList[jobType][1]=STANDARD&refinementList[jobType][2]=TEMPORARY_WORK&page={}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

LOGO_SOCIETE_GENERALE = "https://upload.wikimedia.org/wikipedia/commons/7/7e/Societe_Generale_logo.svg"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'societegenerale'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_html_content(raw_html):
    return BeautifulSoup(html.unescape(raw_html), "lxml").get_text(separator="\n", strip=True)

def get_description_details(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        description_section = soup.find("div", class_="job-description")

        if description_section:
            description = parse_html_content(description_section.get_text())
            return description
        return "Description non disponible"
    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

def get_offer_date(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return datetime.min.date()

        soup = BeautifulSoup(response.text, "html.parser")
        date_section = soup.find("div", class_="job-date")

        if date_section:
            date_text = date_section.get_text(strip=True)
            date_obj = datetime.strptime(date_text, "%d/%m/%Y").date()
            return date_obj
        return datetime.min.date()
    except Exception as e:
        print(f"⚠ Erreur récupération date de l'offre : {e}")
        return datetime.min.date()

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, teletravail):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            "societegenerale", LOGO_SOCIETE_GENERALE, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_societegenerale():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("div", class_="standalone-hit-wrapper")  # Mise à jour pour cibler les bons éléments

        if not job_list_items:
            print("✅ Aucune offre trouvée.")
            break

        for job_item in job_list_items:
            try:
                titre_el = job_item.find("a", class_="js-link-job")
                print(f"📄 Scraping titre {titre_el}")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"

                contrat_el = job_item.find("div", class_="text-white text-base leading-none")
                print(f"📄 Scraping contrat {contrat_el}")
                contrat = contrat_el.get_text(strip=True) if contrat_el else "Non précisé"

                location_el = job_item.find("div", class_="flex items-center gap-2 text-base text-black mask-location-check")
                print(f"📄 Scraping location {location_el}")
                location = location_el.get_text(strip=True) if location_el else "Non précisé"
                ville = location.split(",")[0].strip()

                lieu = "France"  # Le lieu est toujours "France" pour Societe Generale
                lien = f"https://careers.societegenerale.com{job_item.find('a', class_='js-link-job')['href']}"
                description = get_description_details(lien)  # Récupérer la description détaillée
                date_posted = get_offer_date(lien)  # Récupérer la date de publication depuis la page de l'offre
                teletravail = "oui" if "Télétravail possible" in location else "non précisé"

                if date_posted <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                save_offer(titre, contrat, lieu, ville, lien, description, date_posted, teletravail)
                print(f"✅ Offre enregistrée : {titre} ({ville})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_societegenerale()
