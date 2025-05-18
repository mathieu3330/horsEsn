import requests
import psycopg2
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}
# URL pour les offres en alternance
BASE_URL = "https://jobs.sanofi.com/fr/search-jobs/results?ActiveFacetID=0&CurrentPage={}&RecordsPerPage=15&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=True&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=3017382&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=277&FacetFilters%5B0%5D.Display=France&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=Apprentice&FacetFilters%5B1%5D.FacetType=5&FacetFilters%5B1%5D.Count=277&FacetFilters%5B1%5D.Display=Apprentice&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=job_type&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}
LOGO_SANOFI = "https://brandlogos.net/wp-content/uploads/2023/08/sanofi-logo_brandlogos.net_c29es.png"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour analyser le contenu HTML
def parse_html_content(raw_html):
    return BeautifulSoup(raw_html, "lxml").get_text(separator="\n", strip=True)

# Fonction pour récupérer la description complète de l'offre
def get_description_details(offer_url):
    try:
        response = requests.get(offer_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        description_section = soup.find("div", class_="ats-description")

        if description_section:
            description = parse_html_content(description_section.get_text())
            return description
        return "Description non disponible"

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

# Fonction pour récupérer la date de publication de l'offre
def get_offer_date(soup):
    try:
        # Rechercher la date de l'offre
        date_section = soup.find("span", class_="job-date")
        
        if date_section:
            date_text = date_section.get_text(strip=True)
            # Extraction de la date sous le format "janv.. 09, 2025"
            if "Posté le" in date_text:
                date_text = date_text.replace("Posté le", "").strip()
            
            # Mapper le mois en français vers le format anglais pour le parsing
            month_map = {
                "janv..": "Jan",
                "févr..": "Feb",
                "mars": "Mar",
                "avr..": "Apr",
                "mai": "May",
                "juin": "Jun",
                "juil..": "Jul",
                "août": "Aug",
                "sept.": "Sep",
                "oct.": "Oct",
                "nov.": "Nov",
                "déc.": "Dec"
            }
            
            for fr_month, eng_month in month_map.items():
                if fr_month in date_text:
                    date_text = date_text.replace(fr_month, eng_month)
                    break

            # Formater la date pour correspondre au format "YYYY-MM-DD"
            date_obj = datetime.strptime(date_text, "%b. %d, %Y").date()
            return date_obj
        else:
            # Si la date n'est pas présente, retourner la date actuelle
            return datetime.today().date()

    except Exception as e:
        print(f"⚠ Erreur récupération date de l'offre : {e}")
        return datetime.today().date()


# Fonction pour vérifier si l'offre existe déjà dans la base de données
def offer_exists(titre, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM offres WHERE titre = %s AND description = %s AND nomclient = 'sanofi'
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
            "sanofi", LOGO_SANOFI, "prive", teletravail, date_publication
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction principale de scraping
def scrape_sanofi():
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
            results_html = data.get("results", "")

            if not results_html:
                print("✅ Aucune offre trouvée.")
                break

            # Nettoyer les caractères d'échappement
            results_html = results_html.replace("\\r", "").replace("\\n", "").strip()

            # Analyser l'HTML des résultats
            soup = BeautifulSoup(results_html, "html.parser")
            job_list_items = soup.find_all("li")

            if not job_list_items:
                print("✅ Aucune offre trouvée.")
                break

            # Extraire le nombre total de pages
            total_pages = soup.find("section", {"id": "search-results"})["data-total-pages"]
            total_pages = int(total_pages)

            if page > total_pages:
                print("✅ Dernière page atteinte, fin du scraping.")
                break

            for job_item in job_list_items:
                try:
                    titre = job_item.find("h2").get_text(strip=True)
                    contrat = "Alternance"
                    location = job_item.find("span", class_="job-location").get_text(strip=True)

                    # Supprimer "Site:" et extraire uniquement le nom de la ville
                    city = location.replace("Site:", "").strip()

                    lien = f"https://jobs.sanofi.com{job_item.find('a')['href']}"
                    description = get_description_details(lien)  # Récupérer la description détaillée
                    telework = "On-site" if "On-site" in contrat else "non précisé"

                    # Récupérer la date de publication depuis le HTML de l'offre
                    date_posted = get_offer_date(soup)

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
    scrape_sanofi()
