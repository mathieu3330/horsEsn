import requests
import psycopg2
from datetime import datetime
import time
from bs4 import BeautifulSoup

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://careers.danone.com/fr/fr/jobs.html?10000_group.propertyvalues.property=jcr%3Acontent%2Fdata%2Fmaster%2Fcountry&10000_group.propertyvalues.operation=equals&10000_group.propertyvalues.26_values=France&layout=teaserList&p.offset={}&p.limit=12&fulltext=*"
HEADERS = {"User-Agent": "Mozilla/5.0"}

LOGO_DANONE = "https://brandlogos.net/wp-content/uploads/2021/11/danone-logo.png"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'danone'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def parse_html_content(raw_html):
    return BeautifulSoup(raw_html, "lxml").get_text(separator="\n", strip=True)

def get_offer_details(url, titre):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date()

        soup = BeautifulSoup(response.text, "html.parser")

        # Récupération de la description de l'offre
        description_section = soup.find("div", class_="dn-jobdetails__description-body")
        description = description_section.get_text(strip=True) if description_section else "Description non disponible"

        # Informations supplémentaires : Ville
        city = soup.find("h4", class_="job-card__city")
        city = city.get_text(strip=True) if city else "Non précisé"

        # Chercher les mots-clés dans le titre : CDD, CDI, STAGE, ALTERNANCE
        contrat = "Non précisé"
        keywords = ["CDD", "CDI", "STAGE", "ALTERNANCE"]
        for keyword in keywords:
            if keyword.lower() in titre.lower():
                contrat = keyword
                break

        # Si aucun mot-clé n'est trouvé, rechercher dans la balise `dn-jobdetails__positionType`
        if contrat == "Non précisé":
            contrat_section = soup.find("span", class_="dn-jobdetails__positionType")
            contrat = contrat_section.get_text(strip=True) if contrat_section else "Non précisé"

        # Date de publication
        posted_timestamp = soup.find("article")
        posted_date = posted_timestamp.get("posted", "") if posted_timestamp else ""
        try:
            date_pub = datetime.utcfromtimestamp(int(posted_date) / 1000).date() if posted_date else datetime.min.date()
        except Exception as e:
            date_pub = datetime.min.date()

        return description, contrat, city, date_pub

    except Exception as e:
        print(f"⚠ Erreur récupération détails de l'offre : {e}")
        return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date()


    except Exception as e:
        print(f"⚠ Erreur récupération détails de l'offre : {e}")
        return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date()

    except Exception as e:
        print(f"⚠ Erreur récupération détails de l'offre : {e}")
        return "Description non disponible", "Non précisé", "Non précisé", datetime.min.date()

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
            "danone", LOGO_DANONE, "prive", teletravail
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_danone():
    page = 1
    stop_scraping = False
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_list_items = soup.find_all("article", class_="cmp-contentfragment")

        if not job_list_items:
            print("✅ Aucune offre trouvée.")
            break

        for job_item in job_list_items:
            try:
                titre_el = job_item.find("h3", class_="job-card__title")
                titre = titre_el.get_text(strip=True) if titre_el else "Non précisé"

                lien = job_item.find("a", class_="dn-jobdetails__-job-link")["href"] if job_item.find("a", class_="dn-jobdetails__-job-link") else None
                lien = f"https://careers.danone.com{lien}" if lien else None

                description, contrat, ville, date_posted = get_offer_details(lien, titre)

                if date_posted <= last_date:
                    print("⏹ Offre trop ancienne, arrêt.")
                    stop_scraping = True
                    break

                teletravail = "On-site" if "On-site" in contrat else "non précisé"
                save_offer(titre, contrat, "France", ville, lien, description, date_posted, teletravail)
                print(f"✅ Offre enregistrée : {titre} ({ville})")

            except Exception as e:
                print(f"⚠ Erreur traitement offre : {e}")

        page += 12
        time.sleep(1)

if __name__ == "__main__":
    scrape_danone()
