import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
import time

DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://www.safran-group.com/fr/offres?contracts%5B0%5D=39-alternance&contracts%5B1%5D=18-cdd&contracts%5B2%5D=9-cdi&contracts%5B3%5D=42-stage&page={}" 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.safran-group.com",
    "Connection": "keep-alive"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE lien LIKE '%safran-group.com%'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def format_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d.%m.%Y").date()
    except ValueError as e:
        print(f"❌ Erreur format date: {e}")
        return None

def get_offer_description(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("⚠ Erreur récupération description")
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "lxml")
        description_blocks = soup.select(".c-details-offers-container__description--text")
        description_parts = [block.get_text(strip=True, separator=" ") for block in description_blocks]
        return "\n".join(description_parts) if description_parts else "Description non disponible"
    except Exception as e:
        print(f"⚠ Erreur parsing description : {e}")
        return "Description non disponible"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo):
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
            titre, contrat, lieu, ville, lien, description, date_publication,
            "safran", logo, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur insertion : {e}")

def scrape_safran():
    page = 1
    last_date = get_latest_offer_date()
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        print(f"📄 Response.status_code {response.status_code}")
        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="c-offer-item__content")

        if not offres:
            print("✅ Aucune offre trouvée. Fin.")
            break

        for offre in offres:
            try:
                titre_el = offre.find("a", class_="c-offer-item__title")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"
                lien = titre_el["href"] if titre_el and titre_el.has_attr("href") else None

                date_el = offre.find("span", class_="c-offer-item__date")
                date_pub = format_date(date_el.get_text(strip=True)) if date_el else None

                infos = offre.find_all("span", class_="c-offer-item__infos__item")
                entreprise, ville, contrat = "Non précisé", "Non précisé", "Non précisé"
                for info in infos:
                    text = info.get_text(strip=True)
                    if "CDI" in text or "CDD" in text or "Stage" in text or "Alternance" in text:
                        contrat = text
                    elif ", France" in text:
                        ville = text.split(",")[0].strip()
                    elif "Safran" in text:
                        entreprise = text

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, stop.")
                    stop_scraping = True
                    break

                time.sleep(1)
                description = get_offer_description(lien)
                logo = "https://upload.wikimedia.org/wikipedia/fr/0/0e/Logo_Safran.svg"
                lieu = "France"

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo)
                print(f"✅ Offre enregistrée : {titre} ({entreprise})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1

if __name__ == "__main__":
    scrape_safran()
