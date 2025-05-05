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

BASE_URL = "https://choisirleservicepublic.gouv.fr/nos-offres/filtres/localisation/198-200-201-202-219-204-205-196-213-208-199-197-209-214-217/date-de-publication/14_derniers_jours/page/{}/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE lien LIKE '%choisirleservicepublic%'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def format_date(date_str):
    months = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05", "juin": "06",
        "juillet": "07", "août": "08", "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }
    date_str = date_str.lower()
    for fr, num in months.items():
        date_str = date_str.replace(fr, num)
    try:
        return datetime.strptime(date_str.strip(), "%d %m %Y").date()
    except ValueError:
        return None

def get_offer_details(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible", "non précisé", "non précisé", "non précisé"

        soup = BeautifulSoup(response.text, "lxml")

        # --- Récupérer la description ---
        description_parts = []
        missions_section = soup.select_one("div.col-left.rte")
        if missions_section:
            paragraphs = missions_section.find_all(["p", "ul", "li"])
            description_parts.extend(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            hidden_texts = missions_section.find_all("div", {"hidden": True})
            for hidden in hidden_texts:
                paragraphs = hidden.find_all(["p", "ul", "li"])
                description_parts.extend(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        description = "\n".join(description_parts).strip() if description_parts else "Description non disponible"

        # --- Récupérer le contrat ---
        contrat = "non précisé"
        table_items = soup.select("ul.table li")
        for item in table_items:
            strong = item.find("strong")
            if strong and "Nature du contrat" in strong.text:
                if item.find("p"):
                    contrat = item.find("p").get_text(strip=True)
                elif item.find("span"):
                    contrat = item.find_all("span")[-1].get_text(strip=True)
                break

        # --- Récupérer le salaire ---
        salaire = "non précisé"
        salaire_block = soup.select_one("div.salaire")
        if salaire_block:
            results = salaire_block.find_all("span", class_="offer-result")
            for result in results:
                text = result.get_text(strip=True)
                if "€" in text or "euros" in text.lower():
                    salaire = text
                    break

        # --- Récupérer télétravail ---
        teletravail = "non précisé"
        for item in table_items:
            strong = item.find("strong")
            if strong and "Télétravail possible" in strong.text:
                spans = item.find_all("span")
                if spans:
                    teletravail = spans[-1].get_text(strip=True)
                break

        return description, contrat, salaire, teletravail

    except Exception as e:
        print(f"⚠ Erreur récupération détails offre : {e}")
        return "Description non disponible", "non précisé", "non précisé", "non précisé"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo, salaire, teletravail):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail, salaire
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            entreprise, logo, "public", teletravail, salaire
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_service_public():
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
        offres = soup.find_all("div", class_="fr-card--offer")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offre in offres:
            try:
                titre_el = offre.find("h3", class_="fr-card__title")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"

                lien_el = titre_el.find("a") if titre_el else None
                lien = lien_el["href"] if lien_el and lien_el.has_attr("href") else None
                if lien and lien.startswith("/"):
                    lien = "https://choisirleservicepublic.gouv.fr" + lien

                desc_list = offre.find("ul", class_="fr-card__desc")
                items = desc_list.find_all("li") if desc_list else []

                ville, entreprise, date_pub = "Non précisé", "Non précisé", None
                for item in items:
                    text = item.get_text(strip=True)
                    if "Localisation" in text:
                        ville = text.replace("Localisation :", "").strip()
                    elif "Employeur" in text:
                        entreprise = text.replace("Employeur :", "").strip()
                    elif "En ligne depuis" in text:
                        date_text = text.replace("En ligne depuis le", "").strip()
                        date_pub = format_date(date_text)

                lieu = "France"
                logo_el = offre.find("img")
                logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else ""

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt immédiat.")
                    stop_scraping = True
                    break

                time.sleep(1)
                description, contrat, salaire, teletravail = get_offer_details(lien)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo, salaire, teletravail)
                print(f"✅ Offre enregistrée : {titre} ({entreprise})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1

if __name__ == "__main__":
    scrape_service_public()
