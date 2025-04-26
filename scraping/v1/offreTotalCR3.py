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

def get_latest_date_offre():
    """ Récupère la date la plus récente dans la base """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'totalenergies'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]  # datetime object or None

def format_date(date_str):
    """ Convertit 'DD-MM-YYYY' en 'YYYY-MM-DD' """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    except Exception:
        return None

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (titre, contrat, lieu, ville, lien, description, dateoffre, nomclient, logo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (titre, contrat, lieu, ville, lien, description, date_publication, "totalenergies", LOGO_TOTAL))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Offre ajoutée : {titre}")
    except Exception as e:
        print(f"⚠ Erreur d'insertion : {e}")

def scrape_jobs():
    latest_date_offre = get_latest_date_offre()
    print(f"🕒 Dernière date d'offre connue : {latest_date_offre}")
    page = 0

    while True:
        url = f"{BASE_URL}{page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="article article--result")

        if not offres:
            print("✅ Aucune nouvelle offre trouvée.")
            break

        for offre in offres:
            try:
                titre_el = offre.find("h3", class_="article__header__text__title")
                titre = titre_el.text.strip() if titre_el else "Non précisé"
                lien = titre_el.find("a")["href"] if titre_el and titre_el.find("a") else "Aucun lien"
                if lien.startswith("/"):
                    lien = "https://jobs.totalenergies.com" + lien

                contrat = offre.find("li", class_="list-item list-item-employmentType")
                contrat = contrat.text.strip() if contrat else "Non précisé"

                lieu = offre.find("li", class_="list-item list-item-jobCountry")
                lieu = lieu.text.strip() if lieu else "Non précisé"

                date_el = offre.find("li", class_="list-item list-item-jobCreationDate")
                raw_date = date_el.text.strip() if date_el else None
                date_publication = format_date(raw_date)

                # Vérification d'arrêt du scraping
                if latest_date_offre and date_publication and date_publication <= latest_date_offre:
                    print(f"🛑 Offre déjà connue (date : {date_publication}), arrêt du scraping.")
                    return

                ville = "Non précisé"
                description = "Non disponible"

                if lien != "Aucun lien":
                    time.sleep(1)
                    desc_resp = requests.get(lien, headers=HEADERS)
                    if desc_resp.status_code == 200:
                        desc_soup = BeautifulSoup(desc_resp.text, "lxml")
                        for dl in desc_soup.find_all("dl", class_="article__content__view__field"):
                            dt = dl.find("dt", class_="article__content__view__field__label")
                            if dt and "Ville" in dt.text:
                                ville = dl.find("dd", class_="article__content__view__field__value").text.strip()
                                break
                        desc_blocks = desc_soup.find_all("div", class_="article__content js_collapsible__content")
                        descriptions = [p.text.strip() for b in desc_blocks for p in b.find_all("p")]
                        if descriptions:
                            description = "\n".join(descriptions)

                # Insertion en base
                save_offer(titre, contrat, lieu, ville, lien, description, date_publication)

            except Exception as e:
                print(f"⚠ Erreur sur une offre : {e}")

        page += 20

if __name__ == "__main__":
    scrape_jobs()
