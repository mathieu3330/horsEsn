import psycopg2
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def parse_numeric_date(text):
    try:
        return datetime.strptime(text.strip(), "%d.%m.%Y").date()
    except:
        return datetime.today().date()

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE groupeparent = 'Safran'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo, groupeparent):
    try:
        titre = titre or "Non précisé"
        contrat = contrat or "Non précisé"
        ville = ville or "Non précisé"
        lien = lien or "Non précisé"
        description = description or "Non précisé"
        date_publication = date_publication or datetime.today().date()
        entreprise = entreprise or "Non précisé"
        logo = logo or "Non précisé"
        groupeparent = "Safran"

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
            entreprise, logo, "Public", "Non précisé", groupeparent
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Offre insérée : {titre}")
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_safran():
    last_date = get_latest_offer_date()


    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    # Utiliser le chromedriver installé dans l'image
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    stop_scraping = False

    driver.get("https://www.safran-group.com/fr/offres?countries%5B0%5D=1002-france&sort=relevance&page=1")
    try:
        wait = WebDriverWait(driver, 10)
        accept_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cky-btn-accept")))
        accept_btn.click()
        print("✅ Bouton 'Accepter tout' cliqué.")
        time.sleep(2)
    except:
        print("ℹ️ Aucun bouton 'Accepter tout' à cliquer.")

    for page in range(1, 6):
        print(f"\n===== PAGE {page} =====")
        driver.get(f"https://www.safran-group.com/fr/offres?countries%5B0%5D=1002-france&sort=relevance&page={page}")
        time.sleep(20)

        offers = driver.find_elements(By.CLASS_NAME, "c-offer-item__content")

        for offre in offers:
            lieu = "France"
            groupeparent = "Safran"

            try:
                titre = offre.find_element(By.CSS_SELECTOR, "a.c-offer-item__title").text
            except:
                titre = "Non précisé"

            try:
                date_text = offre.find_element(By.CSS_SELECTOR, "span.c-offer-item__date").text
                date_pub = parse_numeric_date(date_text)
            except:
                date_pub = datetime.today().date()

            try:
                infos = offre.find_elements(By.CSS_SELECTOR, "div.c-offer-item__infos span.c-offer-item__infos__item")
                entreprise = infos[0].text if len(infos) > 0 else "Non précisé"
                ville = infos[1].text if len(infos) > 1 else "Non précisé"
                contrat = infos[3].text if len(infos) > 3 else "Non précisé"
                description = "Non précisé"
            except:
                entreprise = "Non précisé"
                ville = "Non précisé"
                contrat = "Non précisé"
                description = "Non précisé"

            try:
                logo = "https://upload.wikimedia.org/wikipedia/fr/5/5f/Safran_-_logo_2016.png"
            except:
                logo = "Non précisé"

            try:
                lien = offre.find_element(By.CSS_SELECTOR, "a.c-offer-item__title").get_attribute("href")
            except:
                lien = "Non précisé"

            print("Titre:", titre)
            print("Date:", date_pub)
            print("Description:", description[:100], "...")
            print("Localisation:", ville)
            print("Contrat:", contrat)
            print("Entreprise:", entreprise)
            print("Logo:", logo)
            print("Lien Offre:", lien)
            print("-" * 80)

            if date_pub <= last_date:
                print("⏹ Offre trop ancienne, arrêt immédiat.")
                driver.quit()
                return

            save_offer(titre, contrat, lieu, ville, lien, description, date_pub, entreprise, logo, groupeparent)


        if stop_scraping == True:
            break
    driver.quit()

if __name__ == "__main__":
    scrape_safran()
