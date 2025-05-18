import requests
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://group.bnpparibas/emploi-carriere/toutes-offres-emploi?page={}&type=2%7C146%7C28%7C36&country=7"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer la dernière date d'offre
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'bnpparibas'")
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
            return "Description non disponible", "Nom Client non trouvé", "BNP Paribas"
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Extraire le nom du client (filiale) dynamiquement
        entity_name_tag = soup.select_one("h1.entity-name")
        entity_name = entity_name_tag.get_text(strip=True) if entity_name_tag else "BNP Paribas"
        
        # Le groupe parent est toujours BNP Paribas
        groupeparent = "BNP Paribas"
        
        description_section = soup.select_one("section.section")

        if description_section:
            paragraphs = description_section.find_all(["p", "ul", "ol", "li", "strong"])
            clean_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            return clean_text if clean_text else "Description non disponible", entity_name, groupeparent
        else:
            return "Description non disponible", entity_name, groupeparent
        
    except Exception as e:
        print(f"⚠ Erreur récupération description : {e}")
        return "Description non disponible", "Nom Client non trouvé", "BNP Paribas"

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo, groupeparent):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail, groupeparent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            entreprise, logo, "prive", "non précisé", groupeparent
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_bnpparibas():
    page = 1
    last_date = get_latest_offer_date()
    stop_scraping = False

    # Configuration de Selenium pour utiliser Chrome en mode headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    while not stop_scraping:
        url = BASE_URL.format(page)
        print(f"📄 Scraping page {page} - URL: {url}")
        driver.get(url)

        # Attendre que la page se charge complètement
        time.sleep(3)

        # Charger le contenu de la page après le JavaScript
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        offres = soup.find_all("article", class_="card-custom card-offer category-146")

        if not offres:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offre in offres:
            try:
                titre = offre.find("h3", class_="title-4").get_text(strip=True)
                print(f"📄 ====== titre {titre} ")

                contrat = offre.find("div", class_="offer-type").get_text(strip=True)
                print(f"📄 ====== contrat {contrat} ")

                location = offre.find("div", class_="offer-location").get_text(strip=True)
                ville = location.split(",")[0].strip()
                lieu = location.split(",")[-1].strip()

                # Extraction de l'URL de l'offre
                lien = "https://group.bnpparibas" + offre.find("a", class_="card-link")["href"]

                # Récupérer le logo de l'offre
                logo_el = offre.find("img")
                logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else ""

                # Vérification si le lien est valide
                if not lien:
                    continue

                date_pub = format_date(offre.get("data-gtm-jobpublishdate", ""))

                if date_pub <= last_date:
                    print("⏹ Offre trop ancienne, arrêt immédiat.")
                    stop_scraping = True
                    break

                # Récupérer la description, le nom client et le groupe parent dynamiquement
                description, entreprise, groupeparent = get_offer_description(lien)

                save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo, groupeparent)
                print(f"✅ Offre enregistrée : {titre} ({entreprise}, {groupeparent})")

            except Exception as e:
                print(f"⚠ Erreur scraping offre : {e}")

        page += 1

    # Fermer le driver Selenium
    driver.quit()

if __name__ == "__main__":
    scrape_bnpparibas()
