import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import time

DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

LOGO_VYV = "https://i.hellowork.com/DQvKZqg5AV5PH06JpaNg_i5LY8gEPGVkkfOjUzPX_iA/w:500/bG9jYWw6Ly8vY3ZjYXRjaGVyL2FkdmVydGlzZXJzL2dyb3VwZV92eXZfY3ZjYXRjaGVyL2JyYW5kcy92eXYzLWxvZ28ucG5n"
BASE_URL = "https://recrutement.groupe-vyv.fr/search?contracts=CDI%2CCDD%2CAlternance%2CStage&page={}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'vyv'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %B %Y").date()
    except Exception:
        try:
            return datetime.strptime(date_str, "%d %b %Y").date()
        except:
            return datetime.today().date()

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, modetravail
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            "vyv", LOGO_VYV, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur insertion BDD : {e}")

def parse_offre_block(a_tag):
    try:
        lien = "https://recrutement.groupe-vyv.fr" + a_tag.get("href")
        titre = a_tag.find("h2").text.strip()

        description_tag = a_tag.find("p")
        description = description_tag.text.strip() if description_tag else "Description non disponible"

        infos = a_tag.find_all("span", class_="sc-fUnMCh")
        ville, contrat = "Non précisé", "Non précisé"
        for info in infos:
            txt = info.get_text(strip=True)
            if txt in ["CDI", "CDD", "Stage", "Alternance"]:
                contrat = txt
            elif txt and not txt.isupper():
                ville = txt

        date_tag = a_tag.find("span").find("span")
        date_pub = parse_date(date_tag.text) if date_tag else datetime.today().date()

        return titre, contrat, "France", ville, lien, description, date_pub
    except Exception as e:
        print(f"⚠ Erreur parsing bloc : {e}")
        return None

def scrape_vyv():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("❌ Erreur HTTP")
            break

        soup = BeautifulSoup(response.text, "lxml")
        a_tags = soup.find_all("a", attrs={"data-testid": "cvc-job-offer-internal-redirection"})
        if not a_tags:
            print("✅ Fin des offres.")
            break

        for a_tag in a_tags:
            parsed = parse_offre_block(a_tag)
            if parsed:
                titre, contrat, lieu, ville, lien, description, date_pub = parsed
                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break
                save_offer(titre, contrat, lieu, ville, lien, description, date_pub)
                print(f"✅ Offre enregistrée : {titre} ({ville})")
        page += 1
        time.sleep(1)

if __name__ == "__main__":
    scrape_vyv()
