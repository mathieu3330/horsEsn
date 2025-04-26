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

BASE_URL = "https://groupecreditagricole.jobs/fr/nos-offres/contrats/577-1292-579/localisations/79/page/{}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'credit_agricole'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def format_date(text):
    try:
        date_text = text.replace("Mis à jour le", "").replace("Modifiée le", "").strip()
        return datetime.strptime(date_text, "%d/%m/%Y").date()
    except ValueError:
        return None

def get_offer_description(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"
        
        soup = BeautifulSoup(response.text, "lxml")
        description_section = soup.select_one("section.block.offer-content.text-container")

        if description_section:
            paragraphs = description_section.find_all(["p", "ul", "ol", "li", "strong"])
            clean_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            return clean_text if clean_text else "Description non disponible"
        else:
            return "Description non disponible"
        
    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo):
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
            titre, contrat, lieu, ville, lien, description, date_publication,
            "credit_agricole", logo, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_credit_agricole():
    page = 1
    last_date = get_latest_offer_date()
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("article", class_="card offer detail")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offre in offres:
            try:
                titre = offre.get("data-gtm-jobtitle", "Non précisé")
                contrat = offre.get("data-gtm-jobcontract", "Non précisé")
                ville = offre.get("data-gtm-jobcity", "Non précisé")
                lieu = offre.get("data-gtm-jobcountry", "Non précisé")
                entreprise = offre.get("data-gtm-jobentity", "Crédit Agricole")
                date_pub = format_date(offre.get("data-gtm-jobpublishdate", ""))

                lien_el = offre.find("a")
                lien = lien_el["href"] if lien_el and lien_el.has_attr("href") else None
                if lien and lien.startswith("/"):
                    lien = "https://groupecreditagricole.jobs" + lien

                logo_el = offre.find("img")
                logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else ""

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt immédiat.")
                    stop_scraping = True
                    break

                time.sleep(1)
                description = get_offer_description(lien)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo)
                print(f"✅ Offre enregistrée : {titre} ({entreprise})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1

if __name__ == "__main__":
    scrape_credit_agricole()
