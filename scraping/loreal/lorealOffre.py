import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
import time

DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}
BASE_URL = "https://careers.loreal.com/fr_FR/jobs/SearchJobsAJAX/?3_110_3=18022&3_33_3=137,134,133,135&jobOffset={}"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE lien LIKE '%careers.loreal.com%'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()


def format_date(date_str):
    try:
        date_str = date_str.lower().replace("publié le", "").replace("publié", "").strip()
        return datetime.strptime(date_str, "%d-%b-%Y").date()
    except ValueError as e:
        print(f"❌ Erreur format date: {e}")
        return None


def get_offer_details(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Non précisé", "Non précisé", "Description non disponible", None

        soup = BeautifulSoup(response.text, "lxml")

        fields = soup.select(".article__content__view__field .article__content__view__field__value")
        contrat, ville, temps, date_pub = "Non précisé", "Non précisé", "Non précisé", None

        if len(fields) >= 6:
            contrat = fields[0].text.strip()
            ville = fields[2].text.strip()
            temps = fields[4].text.strip()
            date_pub = format_date(fields[5].text.strip())

        description_section = soup.find("div", class_="article__content--rich-text")
        if description_section:
            description_parts = description_section.find_all(["p", "ul", "li"])
            description = "\n".join(p.get_text(strip=True) for p in description_parts if p.get_text(strip=True))
        else:
            description = "Description non disponible"

        return contrat, ville, description, date_pub

    except Exception as e:
        print(f"⚠ Erreur récupération détails offre : {e}")
        return "Non précisé", "Non précisé", "Description non disponible", None


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
            "l'oréal", logo, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur insertion : {e}")


def scrape_loreal():
    offset = 0
    last_date = get_latest_offer_date()
    stop_scraping = False

    while not stop_scraping:
        url = BASE_URL.format(offset)
        print(f"📄 Scraping offset {offset} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("article", class_="article--result")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offre in offres:
            try:
                titre_el = offre.find("h3", class_="article__header__text__title")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"

                lien_el = titre_el.find("a") if titre_el else None
                lien = lien_el["href"] if lien_el and lien_el.has_attr("href") else None

                date_el = offre.find("div", class_="article__header__text__subtitle")
                raw_date = date_el.find_all("span")[1].text.strip() if date_el and len(date_el.find_all("span")) > 1 else None
                date_pub = format_date(raw_date) if raw_date else None

                lieu = "France"
                logo = "https://brandlogos.net/wp-content/uploads/2021/11/loreal-logo.png"

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                time.sleep(1)
                contrat, ville, description, date_detail = get_offer_details(lien)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, "l'oréal", logo)
                print(f"✅ Offre enregistrée : {titre}")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        offset += 20


if __name__ == "__main__":
    scrape_loreal()
