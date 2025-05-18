import psycopg2
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def parse_date_us(text):
    try:
        return datetime.strptime(text.strip(), "%m/%d/%Y").date()
    except:
        return datetime.today().date()

def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE groupeparent = 'Publicisgroupe'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur date max:", e)
        return datetime.min.date()

def save_offer(titre, contrat, lieu, ville, lien, description, date_publication, entreprise, logo, groupeparent, ttv):
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
            titre or "Non précisé", contrat or "Non précisé", lieu or "France", ville or "Non précisé",
            lien or "Non précisé", description or "Non précisé", date_publication or datetime.today().date(),
            entreprise or "Non précisé", logo or "Non précisé", "Privé", ttv, groupeparent or "Publicisgroupe"
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Offre insérée : {titre}")
    except Exception as e:
        print(f"⚠ Erreur insertion : {e}")

def get_contrat_from_title(titre):
    titre = titre.lower()
    if "alternant" in titre or "alternance" in titre:
        return "Alternance"
    elif "stage" in titre:
        return "Stage"
    elif "cdd" in titre:
        return "CDD"
    elif "cdi" in titre:
        return "CDI"
    else:
        return "Non précisé"

def extraire_details(driver, url, last_date):
    driver.get(url)
    time.sleep(2)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "ul.meta-data-options.meta-data-top li.meta-data-option"
        )))

        infos = driver.find_elements(By.CSS_SELECTOR, "ul.meta-data-options.meta-data-top li.meta-data-option")
        ville = infos[1].text
        ttv = infos[4].text
        date_pub = infos[5].text
        lieu = "France"
        logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN4h4JiKo5-FOMfY0FLPi2kB0sR6Ti_3wLYg&s"
        groupeparent = "Publicisgroupe"
        entreprise = infos[2].text

        titre = driver.find_element(By.XPATH, '//*[@id="jibe-container"]/div[2]/div/div/h1').text.strip()
        contrat = get_contrat_from_title(titre)

        print("Titre: ", titre)
        print("contrat: ", contrat)
        print("groupeparent: ", groupeparent)

        try:
            description = driver.find_element(By.ID, "description-body").text.strip()
        except:
            description = "Non précisé"

        if date_pub <= last_date:
            print("⏹ Offre trop ancienne, arrêt.")
            return "stop"

        save_offer(titre, contrat, lieu, ville, url, description, date_pub, entreprise, logo, groupeparent, ttv)

    except Exception as e:
        print("⚠️ Erreur dans extraire_details:", e)


def scrape_publicis():
    last_date = get_latest_offer_date()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    # Utiliser le chromedriver installé dans l'image
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    stop_scraping = False



    for page in range(1, 20):
        print(f"\n===== PAGE {page} =====")
        driver.get(f"https://publicisgroupe.jibeapply.com/jobs?location=France&page={page}&stretch=10&stretchUnit=KILOMETERS&woe=12&regionCode=FR")

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.job-title-link")))
            link_elements = driver.find_elements(By.CSS_SELECTOR, "a.job-title-link")
            links = [elem.get_attribute("href") for elem in link_elements if elem.get_attribute("href")]

            for lien in links:
                result = extraire_details(driver, lien, last_date)
                if result == "stop":
                    driver.quit()
                    return
        except:
            print("❌ Erreur lors du chargement de la page.")

    driver.quit()

if __name__ == "__main__":
    scrape_publicis()
