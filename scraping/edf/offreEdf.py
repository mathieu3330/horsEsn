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

BASE_URL = "https://www.edf.fr/edf-recrute/rejoignez-nous/voir-les-offres/nos-offres?search[location]=_TS_CO_Country_France&search[profil][34948]=34948&search[profil][34951]=34951&search[profil][34950]=34950&search[profil][34952]=34952&search[profil][34947]=34947&page={}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE lien LIKE '%edf%'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def format_date(date_str):
    months = {
        "Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06",
        "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"
    }
    for fr, num in months.items():
        date_str = date_str.replace(fr, num)
    try:
        return datetime.strptime(date_str.strip(), "%d %m %Y").date()
    except ValueError:
        return None

def get_offer_description(url):
    try:
        full_url = "https://www.edf.fr" + url if url.startswith("/") else url
        response = requests.get(full_url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible"
        
        soup = BeautifulSoup(response.text, "lxml")
        description_parts = []

        # Partie "Description de l'offre"
        description_section = soup.select_one("div.offer-description")
        if description_section:
            paragraphs = description_section.find_all(["p", "ul", "li", "h2", "h3", "h4"])
            description_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if description_text:
                description_parts.append(description_text)

        # Partie "Profil souhaité"
        profile_section = soup.select_one("div.offer-profile")
        if profile_section:
            paragraphs = profile_section.find_all(["p", "ul", "li", "h2", "h3", "h4"])
            profile_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if profile_text:
                description_parts.append(profile_text)

        full_description = "\n\n".join(description_parts)
        return full_description if full_description else "Description non disponible"

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
            entreprise, logo, "prive", "non précisé"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_edf():
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
        offres = soup.find_all("li", class_="offer")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offre in offres:
            try:
                titre_el = offre.find("h3")
                titre = titre_el.text.strip() if titre_el else "Non précisé"

                date_el = offre.find("div", class_="offer-date")
                date_pub = format_date(date_el.text.strip()) if date_el else None

                lien_el = offre.find("a", class_="offer-link")
                lien = lien_el["href"] if lien_el and lien_el.has_attr("href") else None

                contrat_el = offre.find_all("p")[0] if offre.find_all("p") else None
                contrat = contrat_el.find("span").text.strip() if contrat_el else "Non précisé"

                lieu_el = offre.find_all("p")[1] if len(offre.find_all("p")) > 1 else None
                ville = lieu_el.find("span").text.strip() if lieu_el else "Non précisé"
                lieu = "France"

                logo_el = offre.find("img")
                logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else ""
                entreprise = logo_el["alt"].strip() if logo_el and logo_el.has_attr("alt") else "EDF"

                if not lien or not date_pub:
                    continue

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt immédiat.")
                    stop_scraping = True
                    break

                time.sleep(1)
                description = get_offer_description(lien)

                save_offer(titre, contrat, lieu, ville, "https://www.edf.fr" + lien, description, date_pub, entreprise, logo)
                print(f"✅ Offre enregistrée : {titre} ({entreprise})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1

if __name__ == "__main__":
    scrape_edf()
