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

# URL de base pour Vinci avec pagination
BASE_URL = "https://jobs.vinci.com/fr/search-jobs/results?ActiveFacetID=0&CurrentPage={}&RecordsPerPage=15&TotalContentResults=&Distance=50&RadiusUnitType=1&Keywords=&Location=France&Latitude=46.00000&Longitude=2.00000&ShowRadius=False&IsPagination=True&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=3017382&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=3487&FacetFilters%5B0%5D.Display=France&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=Contrat+%C3%A0+dur%C3%A9e+d%C3%A9termin%C3%A9e&FacetFilters%5B1%5D.FacetType=5&FacetFilters%5B1%5D.Count=82&FacetFilters%5B1%5D.Display=Contrat+%C3%A0+dur%C3%A9e+d%C3%A9termin%C3%A9e&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=job_type&FacetFilters%5B2%5D.ID=Contrat+%C3%A0+dur%C3%A9e+ind%C3%A9termin%C3%A9e&FacetFilters%5B2%5D.FacetType=5&FacetFilters%5B2%5D.Count=2734&FacetFilters%5B2%5D.Display=Contrat+%C3%A0+dur%C3%A9e+ind%C3%A9termin%C3%A9e&FacetFilters%5B2%5D.IsApplied=true&FacetFilters%5B2%5D.FieldName=job_type&FacetFilters%5B3%5D.ID=Contrat+d%27alternance&FacetFilters%5B3%5D.FacetType=5&FacetFilters%5B3%5D.Count=664&FacetFilters%5B3%5D.Display=Contrat+d%27alternance&FacetFilters%5B3%5D.IsApplied=true&FacetFilters%5B3%5D.FieldName=job_type&FacetFilters%5B4%5D.ID=Contrat+de+chantier&FacetFilters%5B4%5D.FacetType=5&FacetFilters%5B4%5D.Count=7&FacetFilters%5B4%5D.Display=Contrat+de+chantier&FacetFilters%5B4%5D.IsApplied=true&FacetFilters%5B4%5D.FieldName=job_type&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=3017382&OrganizationIds=1440&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}
LOGO_VINCI = "https://cdn.worldvectorlogo.com/logos/vinci.svg"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer la dernière date d'offre
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'vinci'")
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

# Fonction pour récupérer la date de publication de l'offre
def get_offer_date(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return datetime.min.date()

        soup = BeautifulSoup(response.text, "html.parser")
        date_section = soup.find("span", class_="job-date job-info job-info--job-date")
        
        if date_section:
            date_text = date_section.get_text(strip=True)
            date_obj = datetime.strptime(date_text, "%d/%m/%Y").date()
            return date_obj
        return datetime.min.date()

    except Exception as e:
        print(f"⚠ Erreur récupération date de l'offre : {e}")
        return datetime.min.date()

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
            "vinci", LOGO_VINCI, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_vinci():
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

            if not results_html:
                print("✅ Aucune offre trouvée.")
                break

            soup = BeautifulSoup(results_html, "html.parser")
            job_list_items = soup.find_all("li", class_="list-item")

            if not job_list_items:
                print("✅ Aucune offre trouvée.")
                break

            for job_item in job_list_items:
                try:
                    titre = job_item.find("span", class_="search-results--link-jobtitle").get_text(strip=True)
                    contrat = job_item.find("span", class_="search-results--link-job-type").get_text(strip=True)
                    location = job_item.find("span", class_="search-results--link-location").get_text(strip=True)
                    city = location.split(",")[0].strip()
                    lien = f"https://jobs.vinci.com{job_item.find('a')['href']}"
                    description = get_description_details(lien)  # Récupérer la description détaillée
                    date_posted = get_offer_date(lien)  # Récupérer la date de publication depuis la page de l'offre
                    telework = "non précisé"  # Ajuster selon les informations de télétravail disponibles

                    if date_posted <= last_date:
                        print("⏹ Offre trop ancienne, arrêt.")
                        stop_scraping = True
                        break

                    save_offer(titre, contrat, "France", city, lien, description, date_posted, telework)
                    print(f"✅ Offre enregistrée : {titre} ({city})")

                except Exception as e:
                    print(f"⚠ Erreur traitement offre : {e}")

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur parsing JSON : {e}")
            break

if __name__ == "__main__":
    scrape_vinci()
