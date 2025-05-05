import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
import time
import html
import json
from http.client import RemoteDisconnected

DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://recrutement.axa.fr/nos-offres-emploi?page={}&LocalContractType=ALTERNANCE,CDD,CDI,STAGE"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}
LOGO_AXA = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/AXA_Logo.svg/2048px-AXA_Logo.svg.png"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'axa'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_html_content(raw_html):
    return BeautifulSoup(html.unescape(raw_html), "lxml").get_text(separator="\n", strip=True)

def detect_teletravail(qualification_html):
    text = parse_html_content(qualification_html).lower()
    if "télétravail" in text or "teletravail" in text:
        return "oui"
    return "non précisé"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, teletravail):
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
            "axa", LOGO_AXA, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_jobs():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()
    seen_ids = set()  # Pour éviter les répétitions
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
        except RemoteDisconnected:
            print("❌ Erreur connexion distante fermée (RemoteDisconnected)")
            break
        except Exception as e:
            print(f"❌ Erreur HTTP: {e}")
            break

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag:
                print("❌ Script JSON non trouvé")
                break

            json_data = json.loads(script_tag.string)
            jobs = json_data["props"]["pageProps"]["jobs"]["data"]

            if not jobs:
                print("✅ Aucune offre trouvée.")
                break

            for job in jobs:
                try:
                    job_id = job.get("RequisitionID")
                    if job_id in seen_ids:
                        print("🔁 Offre déjà vue, arrêt.")
                        stop_scraping = True
                        break
                    seen_ids.add(job_id)

                    titre = job.get("JobTitle", "Non précisé").strip()
                    contrat = job.get("LocalContractType", "Non précisé").strip()
                    lieu = job.get("PrimaryLocationL1", "France").strip()
                    ville = job.get("PrimaryLocationL3", "Non précisé").strip()
                    lien = f"https://recrutement.axa.fr/emploi/{job_id}"
                    raw_description = job.get("JobDescription", "")
                    description = parse_html_content(raw_description)

                    raw_date = job.get("JobOpeningDate", None)
                    date_pub = datetime.fromisoformat(raw_date.split("+")[0]) if raw_date else datetime.now()

                    if date_pub.date() <= last_date:
                        print("⏹ Offre trop ancienne, arrêt.")
                        stop_scraping = True
                        break

                    qualification_html = job.get("JobQualification", "")
                    teletravail = detect_teletravail(qualification_html)

                    save_offer(titre, contrat, lieu, ville, lien, description, date_pub.date(), teletravail)
                    print(f"✅ Offre enregistrée : {titre} ({ville})")

                except Exception as e:
                    print(f"⚠ Erreur traitement offre : {e}")

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur parsing JSON : {e}")
            break

if __name__ == "__main__":
    scrape_jobs()
