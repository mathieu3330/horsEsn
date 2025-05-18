import requests
import psycopg2
from datetime import datetime
import time
from bs4 import BeautifulSoup
import html

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://jobs.veolia.com/fr/search-jobs/results?ActiveFacetID=0&CurrentPage={}&RecordsPerPage=15&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=France&Latitude=46.00000&Longitude=2.00000&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=1&LocationType=2&LocationPath=3017382&OrganizationIds=2702&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

LOGO_VEOLIA = "https://logowik.com/content/uploads/images/veolia7052.jpg"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer la dernière date d'offre
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'veolia'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

# Fonction pour analyser le contenu HTML
def parse_html_content(raw_html):
    return BeautifulSoup(html.unescape(raw_html), "lxml").get_text(separator="\n", strip=True)

# Fonction pour récupérer la description complète de l'offre
def get_description_details(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        description_section = soup.find("div", class_="ats-description")

        if description_section:
            description = description_section.get_text(separator="\n", strip=True)
            return description
        return "Description non disponible"

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

# Fonction pour récupérer la date de publication de l'offre depuis la page de l'offre
def get_offer_date(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return datetime.min.date()

        soup = BeautifulSoup(response.text, "html.parser")
        date_section = soup.find("span", class_="job-date job-info")

        if date_section:
            date_text = date_section.get_text(strip=True).replace("Date de publication", "").strip()
            # Inverser le jour et le mois dans la date
            month, day, year = date_text.split("/")
            date_obj = datetime.strptime(f"{month}/{day}/{year}", "%m/%d/%Y").date()
            return date_obj
        return datetime.min.date()

    except Exception as e:
        print(f"⚠ Erreur récupération date de l'offre : {e}")
        return datetime.min.date()

# Fonction pour vérifier si l'offre existe déjà dans la base de données
def offer_exists(titre, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM offres WHERE titre = %s AND description = %s AND nomclient = 'veolia'
        """, (titre, description))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"⚠ Erreur vérification existence offre : {e}")
        return False

# Fonction pour enregistrer les offres dans la base de données
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
            "veolia", LOGO_VEOLIA, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_veolia():
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

        try:
            # Charger la réponse JSON
            data = response.json()
            results_html = data.get("results", "")
            total_pages = None

            # Extraire le total des pages du contenu HTML (data-total-pages)
            soup = BeautifulSoup(results_html, "html.parser")
            total_pages_tag = soup.find("section", {"id": "search-results"})
            if total_pages_tag:
                total_pages = total_pages_tag.get("data-total-pages", "1")
                total_pages = int(total_pages)

            if not results_html:
                print("✅ Aucune offre trouvée.")
                break

            job_list_items = soup.find_all("li")

            if not job_list_items:
                print("✅ Aucune offre trouvée.")
                break

            for job_item in job_list_items:
                try:
                    titre = job_item.find("h2").get_text(strip=True)
                    location = job_item.find("span", class_="job-location").get_text(strip=True)
                    city = location.replace("Site:", "").strip()
                    lien = f"https://jobs.veolia.com{job_item.find('a')['href']}"
                    description = get_description_details(lien)  # Récupérer la description détaillée
                    date_posted = get_offer_date(lien)  # Récupérer la date de publication depuis la page de l'offre
                    telework = "non précisé"  # Ajuster selon les informations de télétravail disponibles

                    if date_posted <= last_date:
                        print("⏹ Offre trop ancienne, arrêt.")
                        stop_scraping = True
                        break

                    if offer_exists(titre, description):
                        print(f"✅ Offre déjà existante : {titre} ({city})")
                        continue  # Passe à l'offre suivante si elle existe déjà

                    save_offer(titre, "CDI", "France", city, lien, description, date_posted, telework)

                except Exception as e:
                    print(f"⚠ Erreur traitement offre : {e}")

            # Arrêter si on atteint la dernière page
            if page >= total_pages:
                print("✅ Dernière page atteinte.")
                break

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur parsing JSON : {e}")
            break

if __name__ == "__main__":
    scrape_veolia()
