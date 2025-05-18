import requests
import psycopg2
from datetime import datetime
import time
import json

# Configuration de la base de données
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

# URL de base pour Dassault Systèmes avec pagination
BASE_URL = "https://www.3ds.com/apisearch/card_search_api?q=%23all%20card_content_lang%3Afr%20%20%20(card_content_type%3D%22career%22)%20%20card_content_categories%3A(%22pays%2FFrance%22)&s=desc(card_content_start_datetime)&b={}&hf=15&output_format=json"
LOGO_DASSAULT = "https://www.3ds.com/assets/invest/icon-logos/corporate.png"

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer la dernière date d'offre
def get_latest_offer_date():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(dateoffre) FROM offres WHERE nomclient = 'dassault_systèmes'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result[0] else datetime.min.date()
    except Exception as e:
        print("❌ Erreur récupération date:", e)
        return datetime.min.date()

# Fonction pour enregistrer les offres dans la base de données
def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (
                titre, contrat, lieu, ville, lien, description, dateoffre,
                nomclient, logo, secteur
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            titre, contrat, lieu, ville, lien, description, date_publication,
            "dassault_systèmes", LOGO_DASSAULT, "prive"
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

# Fonction pour traiter les données de chaque offre
def extract_offer_data(offer):
    try:
        titre = offer.get("content_title", "Non précisé")
        print(f"⚠ titre ======= : {titre}")
        contrat = offer.get("meta_cat", [])
        contrat = next((item['value'] for item in contrat if 'Apprentissage' in item['value']), "Non précisé")
        lieu = "France"  # En supposant que toutes les offres sont en France
        ville = next((item['value'] for item in offer.get("meta_cat", []) if "Vélizy-Villacoublay" in item['value']), "Non précisé")
        lien = f"https://www.3ds.com/fr/careers/jobs/{offer.get('url')}"
        description = offer.get("content_summary", "Description non disponible")  # Peut être améliorée selon les besoins
        date_posted = offer.get("content_start_datetime", "")
        if date_posted:
            date_posted = datetime.strptime(date_posted, "%Y/%m/%d %H:%M:%S").date()
        else:
            date_posted = datetime.min.date()

        return titre, contrat, lieu, ville, lien, description, date_posted

    except Exception as e:
        print(f"⚠ Erreur lors du traitement de l'offre : {e}")
        return None

# Fonction pour scraper une page d'offres
def scrape_page(page_start):
    url = BASE_URL.format(page_start)
    print(f"📄 Scraping page {page_start} - URL: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Erreur HTTP. Fin du scraping.")
        return []

    try:
        # Vérifier si la réponse est bien un JSON
        try:
            data = response.json()
        except ValueError as e:
            print(f"❌ Erreur parsing JSON: {e}")
            return []

        results = data.get("context", {}).get("hits", [])

        offers_data = []
        for offer in results:
            offer_data = extract_offer_data(offer)
            if offer_data:
                offers_data.append(offer_data)

        return offers_data
    except Exception as e:
        print(f"❌ Erreur parsing JSON : {e}")
        return []

# Fonction principale de scraping
def scrape_dassault_systèmes():
    page = 0
    stop_scraping = False
    last_date = get_latest_offer_date()
    print(f"⏹ Date MAX(dateoffre) = : {last_date}")

    while not stop_scraping:
        offers_data = scrape_page(page)

        if not offers_data:
            print("✅ Aucune offre trouvée. Fin du scraping.")
            break

        for offer_data in offers_data:
            titre, contrat, lieu, ville, lien, description, date_posted = offer_data

            if date_posted <= last_date:
                print("⏹ Offre trop ancienne, arrêt.")
                stop_scraping = True
                break

            save_offer(titre, contrat, lieu, ville, lien, description, date_posted)
            print(f"✅ Offre enregistrée : {titre} ({ville})")

        page += 15  # Passer à la page suivante
        time.sleep(1)

if __name__ == "__main__":
    scrape_dassault_systèmes()
