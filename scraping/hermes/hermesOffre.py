import requests
import psycopg2
from datetime import datetime
import time
import html
import json
from bs4 import BeautifulSoup

DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

LOGO_HERMES = "https://brandlogos.net/wp-content/uploads/2018/10/hermes-logo.png"

API_LIST_URL = (
    "https://fa-eoic-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
    "?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,"
    "requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields"
    "&finder=findReqs;siteNumber=CX_12001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES"
    "%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=7,lastSelectedFacet=LOCATIONS,"
    "selectedFlexFieldsFacets=%22AttributeChar5%7CUnlimited%20contract%3BApprenticeship%20contract%3BInternship%20"
    "contract%3BLimited%20contract%22,selectedLocationsFacet=300000000385300,sortBy=POSTING_DATES_DESC,offset={}"
)

API_DETAIL_URL = "https://fa-eoic-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?onlyData=true&expand=all&finder=ById;Id=\"{}\",siteNumber=CX_12001"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'hermes'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_html_content(raw_html):
    return BeautifulSoup(html.unescape(raw_html), "lxml").get_text(separator="\n", strip=True)

def get_description(job_id):
    try:
        url = API_DETAIL_URL.format(job_id)
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible", "non précisé", "Non précisé"

        data = response.json()
        items = data.get("items", [])
        if not items:
            return "Description non disponible", "non précisé", "Non précisé"

        item = items[0]
        description_html = item.get("ExternalDescriptionStr", "")
        description = parse_html_content(description_html)

        # 🔍 Télétravail
        teletravail = "oui" if "télétravail" in description.lower() else "non précisé"

        # 🔍 Contrat
        contrat = item.get("RequisitionType", "").strip()
        if not contrat:
            for field in item.get("requisitionFlexFields", []):
                if field.get("Prompt", "").strip().lower() == "type de contrat":
                    contrat = field.get("Value", "Non précisé").strip()
                    break
        if not contrat:
            contrat = "Non précisé"

        return description, teletravail, contrat

    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible", "non précisé", "Non précisé"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, teletravail):
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
            "hermes", LOGO_HERMES, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur insertion BDD : {e}")

def scrape_hermes():
    offset = 0
    stop_scraping = False
    last_date = get_latest_offer_date()

    while not stop_scraping:
        url = API_LIST_URL.format(offset)
        print(f"🔎 Scraping offset={offset} - {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP")
            break

        data = response.json()

        jobs = data.get("items", [])[0].get("requisitionList", [])
        if not any(job.get("Id") for job in jobs):
             print("✅ Fin des offres (aucune offre valide).")
             break

        for job in jobs:
            try:
                titre = job.get("Title", "Non précisé").strip()
                ville = job.get("PrimaryLocation", "Non précisé")
                lieu = "France"
                date_pub = datetime.strptime(job.get("PostedDate", "1970-01-01"), "%Y-%m-%d").date()

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                lien = f"https://www.hermes.com/fr/fr/talents/offres/{job.get('Id')}/"
                description, teletravail, contrat = get_description(job.get("Id"))

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, teletravail)
                print(f"✅ Offre enregistrée : {titre} ({ville})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        offset += 7
        time.sleep(1)

if __name__ == "__main__":
    scrape_hermes()
