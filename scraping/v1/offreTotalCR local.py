import os
import requests
import psycopg2
from bs4 import BeautifulSoup
import time

# Configuration de la base de données
#DB_CONFIG = {
#    "host": "/cloudsql/horsesn:us-central1:projectdinterne",
#    "port": "5432",
#    "dbname": "postgres",
#    "user": "postgres",
#    "password": "root"  # Replace with the real password
#}


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}


# URL de base des offres
BASE_URL = "https://jobs.totalenergies.com/fr_FR/careers/SearchJobs/?707=%5B42253%2C357336%2C42258%5D&707_format=1393&3834=%5B41588%5D&3834_format=3639&listFilterMode=1&jobRecordsPerPage=20&#jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def get_db_connection():
    """ Établit une connexion avec la base PostgreSQL """
    return psycopg2.connect(**DB_CONFIG)

def save_offer(titre, contrat, lieu, lien, description):
    """ Insère une offre d'emploi dans la base de données """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (titre, contrat, lieu, lien, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (titre, contrat, lieu, lien, description))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion dans la base : {e}")

def scrape_jobs():
    """ Scrape les offres d'emploi et les enregistre en base """
    page = 0  
    while True:
        url = f"{BASE_URL}{page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Fin du scraping. Erreur HTTP.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="article article--result")

        if not offres:
            print(f"✅ Fin du scraping. Dernière page : {page // 20}")
            break

        print(f"📌 Scraping de la page {page // 20 + 1}... ({len(offres)} offres trouvées)")

        for offre in offres:
            try:
                titre_element = offre.find("h3", class_="article__header__text__title")
                titre = titre_element.text.strip() if titre_element else "Non précisé"
                lien = titre_element.find("a")["href"] if titre_element and titre_element.find("a") else "Aucun lien"
                if lien.startswith("/"):
                    lien = "https://jobs.totalenergies.com" + lien

                contrat = offre.find("li", class_="list-item list-item-employmentType").text.strip() if offre.find("li", class_="list-item list-item-employmentType") else "Non précisé"
                lieu = offre.find("li", class_="list-item list-item-jobCountry").text.strip() if offre.find("li", class_="list-item list-item-jobCountry") else "Non précisé"

                # Récupérer la description
                description = "Non disponible"
                if lien != "Aucun lien":
                    time.sleep(1)
                    desc_response = requests.get(lien, headers=HEADERS)
                    if desc_response.status_code == 200:
                        desc_soup = BeautifulSoup(desc_response.text, "lxml")
                        desc_blocks = desc_soup.find_all("div", class_="article__content js_collapsible__content")
                        descriptions = [para.text.strip() for block in desc_blocks for para in block.find_all("p")]
                        if descriptions:
                            description = "\n".join(descriptions)

                save_offer(titre, contrat, lieu, lien, description)
            except Exception as e:
                print(f"⚠ Erreur lors de la récupération d'une offre : {e}")

        page += 20  

if __name__ == "__main__":
    scrape_jobs()
