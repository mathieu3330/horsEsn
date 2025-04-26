import os
import requests
import psycopg2
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Configuration de la base de données
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

BASE_URL = "https://jobs.totalenergies.com/fr_FR/careers/SearchJobs/?707=%5B42253%2C42258%2C357336%5D&707_format=1393&3834=%5B41588%5D&3834_format=3639&listFilterMode=1&jobRecordsPerPage=20&jobOffset="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def format_date(date_str):
    """ Convertit une date du format 'DD-MM-YYYY' vers 'YYYY-MM-DD' pour PostgreSQL """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return "0000-00-00"  # Valeur par défaut si la conversion échoue


def save_offer(titre, contrat, lieu, ville, lien, description, date_publication):
    """ Insère une offre en base de données """
    print(f"============= Ville ========== {ville}")
    print(f"============= Date de publication ========== {date_publication}")
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offres (titre, contrat, lieu, ville, lien, description, dateOffre, nomClient)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (titre, contrat, lieu, ville, lien, description, date_publication, "totalenergies"))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Erreur lors de l'insertion : {e}")

def scrape_jobs():
    """ Scrape les offres d'emploi et les enregistre en base """
    page = 0  
    while True:
        url = f"{BASE_URL}{page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Erreur HTTP. Fin du scraping.")
            break

        soup = BeautifulSoup(response.text, "lxml")
        offres = soup.find_all("div", class_="article article--result")

        if not offres:
            print(f"✅ Fin du scraping. Dernière page : {page // 20}")
            break

        print(f"📌 Scraping de la page {page // 20 + 1}... ({len(offres)} offres trouvées)")

        for offre in offres:
            try:
                # 📌 Récupérer le titre et le lien
                titre_element = offre.find("h3", class_="article__header__text__title")
                titre = titre_element.text.strip() if titre_element else "Non précisé"
                lien = titre_element.find("a")["href"] if titre_element and titre_element.find("a") else "Aucun lien"
                if lien.startswith("/"):
                    lien = "https://jobs.totalenergies.com" + lien

                # 📌 Récupérer le type de contrat
                contrat = offre.find("li", class_="list-item list-item-employmentType")
                contrat = contrat.text.strip() if contrat else "Non précisé"

                # 📌 Récupérer le lieu (Pays)
                lieu = offre.find("li", class_="list-item list-item-jobCountry")
                lieu = lieu.text.strip() if lieu else "Non précisé"

                # 📌 Récupérer la date de publication
                date_element = offre.find("li", class_="list-item list-item-jobCreationDate")
                date_publication = date_element.text.strip() if date_element else "Non précisé"
                # Conversion de la date pour PostgreSQL
                if date_publication != "Non précisé":
                   date_publication = format_date(date_publication)

                # 📌 Initialisation des valeurs de ville et description
                ville = "Non précisé"
                description = "Non disponible"

                if lien != "Aucun lien":
                    time.sleep(1)  # Pause pour éviter le blocage
                    desc_response = requests.get(lien, headers=HEADERS)
                    if desc_response.status_code == 200:
                        desc_soup = BeautifulSoup(desc_response.text, "lxml")

                        # 🔹 Trouver la ville
                        for dl in desc_soup.find_all("dl", class_="article__content__view__field"):
                            dt = dl.find("dt", class_="article__content__view__field__label")
                            if dt and "Ville" in dt.text:
                                ville = dl.find("dd", class_="article__content__view__field__value").text.strip()
                                break  # Stop dès qu'on trouve

                        # 🔹 Récupérer la description
                        desc_blocks = desc_soup.find_all("div", class_="article__content js_collapsible__content")
                        descriptions = [para.text.strip() for block in desc_blocks for para in block.find_all("p")]
                        if descriptions:
                            description = "\n".join(descriptions)

                # 📌 Sauvegarde en base
                save_offer(titre, contrat, lieu, ville, lien, description, date_publication)

            except Exception as e:
                print(f"⚠ Erreur lors du scraping d'une offre : {e}")

        page += 20  # Passer à la page suivante

if __name__ == "__main__":
    scrape_jobs()
