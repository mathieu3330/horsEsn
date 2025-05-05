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
HEADERS = {"User-Agent": "Mozilla/5.0"}


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


def format_date_safran(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d.%m.%Y").date()
    except ValueError as e:
        print(f"❌ Erreur format date: {e}")
        return None


def get_offer_details(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"

        soup = BeautifulSoup(response.text, "lxml")
        blocks = soup.select("div.c-details-offers-container__description--text")
        paragraphs = []
        for block in blocks:
            paragraphs += block.find_all(["p", "ul", "li"])

        description = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return description if description else "Description non disponible"
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
        print(f"⚠ Erreur lors de l'insertion : {e}")


def scrape_safran():
  
    page = 1
    last_date = get_latest_offer_date()
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)
        print(f"✅ Statut HTTP test: {response.status_code}")

        if response.status_code != 200:
            print("❌ Erreur HTTP toto. Fin. {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.select("div.c-offer-item__content")

        if not offres:
            print("✅ Aucune offre trouvée. Fin.")
            break

        for offre in offres:
            try:
                titre_el = offre.select_one("a.c-offer-item__title")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"
                lien = titre_el["href"] if titre_el and titre_el.has_attr("href") else None

                date_el = offre.select_one("span.c-offer-item__date")
                date_pub = format_date_safran(date_el.text.strip()) if date_el else None

                infos = offre.select(".c-offer-item__infos__item")
                entreprise, ville, contrat = "", "", ""
                for info in infos:
                    text = info.get_text(strip=True)
                    if "Safran" in text:
                        entreprise = text
                    elif "CDI" in text or "CDD" in text or "Alternance" in text or "Stage" in text:
                        contrat = text
                    elif "," in text and "France" in text:
                        ville = text

                lieu = "France"
                logo = "https://www.safran-group.com/themes/custom/safran_theme/logo.svg"

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                time.sleep(1)
                description = get_offer_details(lien)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo)
                print(f"✅ Offre enregistrée : {titre} ({entreprise})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1


if __name__ == "__main__":
    # Test accessibilité
    test_url = BASE_URL.format(1)
    try:
        r = requests.get(test_url, headers=HEADERS)
        print(f"✅ Statut HTTP test: {r.status_code}")
        print(r.text[:500])
    except Exception as e:
        print(f"❌ Erreur de connexion au site Safran : {e}")

    # Lancer le scraping réel
    scrape_safran()
