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

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

LOGO_NESTLE = "https://logo-marque.com/wp-content/uploads/2020/09/Nestle-Logo.png"
LOGO_NESPRESSO = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7wJJ3lVOVnppDUDT6aQynwWgK98nLdTsnFg&s"
LOGO_PURINA = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-1vTH9694tY4cOwiU6UGMatBr713plNQqig&s"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Vérification si l'offre existe déjà dans la base de données (par titre + description + contrat + groupe)
def offer_exists(titre, description, contrat):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM offres WHERE titre = %s AND description = %s AND contrat = %s 
        """, (titre, description, contrat))
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result > 0
    except Exception as e:
        print(f"⚠ Erreur vérification doublon : {e}")
        return False

# Fonction pour récupérer la description détaillée de l'offre
def get_description(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "html.parser")
        description_section = soup.find("span", class_="jobdescription")

        if description_section:
            description = description_section.get_text(separator="\n", strip=True)
            return description
        return "Description non disponible"

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

# Fonction pour récupérer le type de contrat à partir du titre et de la section "career-area"
def get_contrat_from_title(titre, job_item):
    if "alternant" in titre.lower():
        # Vérification dans "career-area" si c'est réellement un contrat en alternance
        career_area = job_item.find("div", class_="jobs-career-area")
        if career_area and "internships/apprenticeships" in career_area.get_text(strip=True).lower():
            return "Alternance"
        return "Stage"  # Par défaut, si le titre contient "alternant", mais la carrière n'est pas précisée
    elif "stage" in titre.lower():
        return "Stage"
    elif "cdd" in titre.lower():
        return "CDD"
    else:
        return "CDI"

# Fonction pour enregistrer les offres dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, teletravail, nomclient, logo, groupeparent):
    try:

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

# Fonction pour scraper Nestlé
def scrape_nestle():
    page = 0
    base_url = "https://www.nestle.fr/jobs/search-jobs?keyword=&country=FR&location=&career_area=All&page=%2C{}"
    
    while True:
        url = base_url.format(page)
        print(f"🔎 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("div", class_="jobs-container views-row")

        if not job_list_items:
            print("✅ Fin des offres.")
            break

        for job_item in job_list_items:
            try:
                # Récupérer titre
                titre = job_item.find("div", class_="jobs-title").get_text(strip=True)
                # Récupérer description
                lien = job_item.find("a")["href"]
                description = get_description(lien)

                # Si le titre ou la description est vide, on arrête le traitement de cette offre
                if not titre and not description:
                    print(f"⚠ Offre sans titre ou description valide, passage à l'offre suivante.")
                    break

                contrat = get_contrat_from_title(titre, job_item)  # Récupérer le contrat depuis le titre et "career-area"
                ville = job_item.find("div", class_="jobs-location").get_text(strip=True)
                lieu = "France"
                date_posted = datetime.now().date()  # Utiliser la date actuelle
                teletravail = "Oui" if "télétravail" in description.lower() else "Non"
                nomclient = job_item.find("div", class_="jobs-business").get_text(strip=True)
                
                # Déterminer le logo à utiliser en fonction de la filiale
                if "Nespresso" in nomclient:
                    logo = LOGO_NESPRESSO
                    groupeparent = "Nestlé"
                elif "Purina" in nomclient:
                    logo = LOGO_PURINA
                    groupeparent = "Nestlé"
                else:
                    logo = LOGO_NESTLE
                    groupeparent = "Nestlé"

                # Vérification de l'existence de l'offre avant d'insérer
                if offer_exists(titre, description, contrat):
                    print(f"⚠ Offre déjà présente : {titre}{contrat}{groupeparent}")
                else:   
                    save_offer(titre, contrat, lieu, ville, lien, description, date_posted, teletravail, nomclient, logo, groupeparent)

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_nestle()
