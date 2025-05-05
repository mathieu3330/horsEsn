import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
import html
import time
import re

DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://jobs.groupe-psa.com/offre-de-emploi/liste-offres.aspx?page={}&LCID=1036"
DETAIL_URL_BASE = "https://jobs.groupe-psa.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
LOGO_PSA = "https://brandlogos.net/wp-content/uploads/2021/11/stellantis-logo.png"


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'psa'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()


def parse_html_content(raw_html):
    return BeautifulSoup(html.unescape(raw_html), "lxml").get_text(separator="\n", strip=True)


def extract_date_from_meta(soup):
    meta = soup.find("meta", {"name": "Description"})
    if meta and "Date" in meta.get("content", ""):
        match = re.search(r"Date\s*:\s*(\d{2}/\d{2}/\d{4})", meta["content"])
        if match:
            return datetime.strptime(match.group(1), "%d/%m/%Y").date()
    return datetime.today().date()


def get_description_and_date(relative_url):
    try:
        url = DETAIL_URL_BASE + relative_url
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible", datetime.today().date()

        soup = BeautifulSoup(response.text, "html.parser")
        date_pub = extract_date_from_meta(soup)
        desc_tag = soup.find("p", id="fldjobdescription_description1")
        description = parse_html_content(str(desc_tag)) if desc_tag else "Description non disponible"
        return description, date_pub
    except Exception as e:
        print(f"⚠ Erreur description: {e}")
        return "Description non disponible", datetime.today().date()


def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
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
            "psa", LOGO_PSA, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur insertion BDD : {e}")


def scrape_jobs():
    page = 1
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")
    seen_links = set()

    while True:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="ts-offer-card")

        if not cards:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        stop_scraping = False
        for card in cards:
            try:
                title_tag = card.find("h3", class_="ts-offer-card__title")
                if not title_tag:
                    continue

                link_tag = title_tag.find("a")
                if not link_tag:
                    continue

                titre = link_tag.text.strip()
                relative_url = link_tag["href"]
                lien = DETAIL_URL_BASE + relative_url

                if lien in seen_links:
                    print("🔁 Offre déjà vue, arrêt.")
                    stop_scraping = True
                    break
                seen_links.add(lien)

                details = card.find("ul", class_="ts-offer-card-content__list")
                li_items = details.find_all("li") if details else []

                contrat = li_items[1].text.strip() if len(li_items) > 1 else "Non précisé"
                ville = li_items[2].text.strip() if len(li_items) > 2 else "Non précisé"
                lieu = "France"

                description, date_pub = get_description_and_date(relative_url)

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub)
                print(f"✅ Offre enregistrée : {titre} ({ville})")
            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        if stop_scraping:
            break

        page += 1
        time.sleep(1)


if __name__ == "__main__":
    scrape_jobs()
