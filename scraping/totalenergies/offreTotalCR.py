import os
import requests
import psycopg2
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://jobs.totalenergies.com/fr_FR/careers/SearchJobs/?707=%5B42253%2C42258%2C357336%5D&707_format=1393&3834=%5B41588%5D&3834_format=3639&listFilterMode=1&jobRecordsPerPage=20&jobOffset="
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LOGO_TOTAL = "https://upload.wikimedia.org/wikipedia/fr/thumb/f/f7/Logo_TotalEnergies.svg/2000px-Logo_TotalEnergies.svg.png"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'totalenergies'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        dateMax= result[0] if result[0] else datetime.min.date() 
        
        print("⏹ Date MAX(dateoffre) =   : ", dateMax)
    
        return result[0] if result[0] else datetime.min.date()  

    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return None
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre,
            contrat,
            lieu,
            ville,
            lien,
            description,
            date_publication,
            "totalenergies",
            LOGO_TOTAL,
            "prive",         # 👈 Secteur privé
            "non précisé"    # 👈 Mode de travail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")



def scrape_jobs():
    page = 0
    last_date = get_latest_offer_date()
    print(f"🗓 Dernière date en base : {last_date}")

    stop_scraping = False

    while not stop_scraping:
        url = f"{BASE_URL}{page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="article article--result")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        print(f"🔍 Page {page // 20 + 1} – {len(offres)} offres")

        for offre in offres:
            try:
                titre_element = offre.find("h3", class_="article__header__text__title")
                titre = titre_element.text.strip() if titre_element else "Non précisé"

                if "Aucun emploi" in titre:
                    continue

                lien = titre_element.find("a")["href"] if titre_element and titre_element.find("a") else "Aucun lien"
                if lien.startswith("/"):
                    lien = "https://jobs.totalenergies.com" + lien

                contrat = offre.find("li", class_="list-item list-item-employmentType")
                contrat = contrat.text.strip() if contrat else "Non précisé"

                lieu = offre.find("li", class_="list-item list-item-jobCountry")
                lieu = lieu.text.strip() if lieu else "Non précisé"

                date_element = offre.find("li", class_="list-item list-item-jobCreationDate")
                date_pub = format_date(date_element.text.strip()) if date_element else None

                if not date_pub or date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt immédiat.")
                    stop_scraping = True
                    break

                ville = "Non précisé"
                description = "Non disponible"

                if lien != "Aucun lien":
                    time.sleep(1)
                    desc_response = requests.get(lien, headers=HEADERS)
                    if desc_response.status_code == 200:
                        desc_soup = BeautifulSoup(desc_response.text, "lxml")
                        for dl in desc_soup.find_all("dl", class_="article__content__view__field"):
                            dt = dl.find("dt", class_="article__content__view__field__label")
                            if dt and "Ville" in dt.text:
                                dd = dl.find("dd", class_="article__content__view__field__value")
                                if dd:
                                    ville = dd.text.strip()
                                    break
                        desc_blocks = desc_soup.find_all("div", class_="article__content js_collapsible__content")
                        descriptions = [p.text.strip() for block in desc_blocks for p in block.find_all("p")]
                        if descriptions:
                            description = "\n".join(descriptions)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub)

            except Exception as e:
                print(f"⚠ Erreur scraping d'une offre : {e}")

        page += 20

if __name__ == "__main__":
    scrape_jobs()
