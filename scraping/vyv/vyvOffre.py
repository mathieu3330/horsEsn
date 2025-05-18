import psycopg2
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

# Connexion à la base
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def parse_french_date(text):
    mois = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }

    parts = text.strip().lower().split()
    if len(parts) == 3:
        jour, mois_fr, annee = parts
        mois_num = mois.get(mois_fr)
        if mois_num:
            date_str = f"{jour}/{mois_num}/{annee}"
            return datetime.strptime(date_str, "%d/%m/%Y").date()
    return datetime.today().date()  # fallback


# Récupérer la dernière date d'insertion
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE groupeparent = 'VYV'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

# Sauvegarder une offre dans la base
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo, groupeparent):

    try:
        titre = titre or "Non précisé"
        contrat = contrat or "Non précisé"
        lieu = lieu or "France"
        ville = ville or "Non précisé"
        lien = lien or "Non précisé"
        description = description or "Non précisé"
        date_publication = date_publication or datetime.today().date()
        entreprise = entreprise or "Non précisé"
        logo = logo or "Non précisé"
        groupeparent = groupeparent or "VYV"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur, teletravail, groupeparent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, "France", ville, lien, description, date_publication,
            entreprise, logo, "Prive", "Non précisé", groupeparent
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Offre insérée : {titre}")
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Scraper les offres VYV
def scrape_vyv():
    last_date = get_latest_offer_date()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    # Utiliser le chromedriver installé dans l'image
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    stop_scraping = False

    for page in range(1, 126):

        print(f"\n===== PAGE {page} =====")
        driver.get(f"https://recrutement.groupe-vyv.fr/search?page={page}")
        time.sleep(20)
        offres = driver.find_elements(By.CSS_SELECTOR, "div.sc-kCMKrZ.dHHUFF")

        for offre in offres:

            lieu = "France"
            teletravail = "Non précisé"
            groupeparent = "VYV"
            secteur = "Prive"

            try:
                titre = offre.find_element(By.CSS_SELECTOR, "h2").text
            except:
                titre = "Non précisé"

            try:
                date_text = offre.find_element(By.CSS_SELECTOR, "span[mode='secondary']").text
                date_pub = parse_french_date(date_text)
            except:
                date_pub = "Non précisé"

            try:
                description = offre.find_element(By.CSS_SELECTOR, "p").text
            except:
                description = "Non précisé"

            try:
                spans = offre.find_elements(By.CSS_SELECTOR, "span.sc-fUnMCh span")
                location_1 = spans[1].text if len(spans) > 1 else "Non précisé"
                contrat_1 = spans[2].text if len(spans) > 2 else "Non précisé"  # "Entreprise non trouvée"
                entreprise = spans[3].text if len(spans) > 2 else "Non précisé"
            except:
                location_1 = "Non précisé"
                contrat_1 = "Non précisé"
                entreprise = "Non précisé"

            try:
                logo = offre.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            except:
                logo = "Non précisé"

            try:
                lien_offre = offre.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                lien_offre = "Non précisé"

            print("-" * 80)


            if date_pub <= last_date:
                print("⏹ Offre trop ancienne, arrêt immédiat.")
                driver.quit()
                stop_scraping = True
                break

            save_offer(titre, contrat_1, "France", location_1, lien_offre, description, date_pub, entreprise, logo, "VYV")

        if stop_scraping == True:
            break

    driver.quit()

if __name__ == "__main__":
    scrape_vyv()
