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

BASE_URL = "https://group.bnpparibas/emploi-carriere/toutes-offres-emploi"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LOGO_BNP_PARIBAS = "https://upload.wikimedia.org/wikipedia/fr/thumb/8/8e/Logo_BNP_Paribas.svg/1200px-Logo_BNP_Paribas.svg.png"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'bnpparibas'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        dateMax = result[0] if result[0] else datetime.min.date()
        print("⏹ Date MAX(dateoffre) =   : ", dateMax)
        return dateMax
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
                nomclient, logo, secteur, modetravail
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
            "bnpparibas",
            LOGO_BNP_PARIBAS,
            "prive",
            "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_jobs():
    page = 1
    last_date = get_latest_offer_date()
    print(f"🗓 Dernière date en base : {last_date}")

    stop_scraping = False

    while not stop_scraping:
        params = {
            "page": page,
            "type": "2|146|28|36",  # Types de contrat : CDI, CDD, Stage, Alternance
            "country": "7"          # Pays : France
        }
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("article", class_="card-custom card-offer")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        print(f"🔍 Page {page} – {len(offres)} offres")

        for offre in offres:
            try:
                titre_element = offre.find("h3", class_="title-4")
                titre = titre_element.text.strip() if titre_element else "Non précisé"

                lien_tag = offre.find("a", class_="card-link")
                lien = "https://group.bnpparibas" + lien_tag["href"] if lien_tag else "Aucun lien"

                contrat_tag = offre.find("div", class_="offer-type")
                contrat = contrat_tag.text.strip() if contrat_tag else "Non précisé"

                location_tag = offre.find("div", class_="offer-location")
                lieu = location_tag.text.strip() if location_tag else "Non précisé"

                # BNP Paribas ne fournit pas la date de publication directement, on utilise la date du jour
                date_pub = datetime.today().date()

                if date_pub <= last_date:
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
                        # Extraction de la ville si disponible
                        location_detail = desc_soup.find("div", class_="offer-location")
                        if location_detail:
                            ville = location_detail.text.strip()
                        # Extraction de la description
                        desc_section = desc_soup.find("div", class_="offer-description")
                        if desc_section:
                            paragraphs = desc_section.find_all("p")
                            descriptions = [p.text.strip() for p in paragraphs]
                            if descriptions:
                                description = "\n".join(descriptions)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub)

            except Exception as e:
                print(f"⚠ Erreur scraping d'une offre : {e}")

        page += 1
        time.sleep(1)  # Pause pour éviter de surcharger le serveur

if __name__ == "__main__":
    scrape_jobs()
