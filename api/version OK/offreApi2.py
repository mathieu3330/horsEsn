import os
from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# 🔹 Connexion à Cloud SQL via Cloud Run
DB_CONFIG = {
    "host": "/cloudsql/projetdbt-450020:us-central1:projetcdinterne",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_db_connection():
    """ Établit une connexion PostgreSQL """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.get("/")
def read_root():
    return {"message": "API de gestion des offres d'emploi"}

@app.get("/offres")
def get_offres(contrat: str = Query(None), ville: str = Query(None), search: str = Query(None)):
    """ Récupère toutes les offres avec filtres facultatifs et recherche Full-Text """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM offres 
        WHERE 1=1
    """
    params = []

    if contrat:
        query += " AND contrat = %s"
        params.append(contrat)
    if ville:
        query += " AND ville = %s"
        params.append(ville)
    if search:
        query += " AND to_tsvector('french', titre || ' ' || description) @@ plainto_tsquery('french', %s)"
        params.append(search)

    query += " ORDER BY dateScraping DESC"  # Trier par date la plus récente

    cursor.execute(query, tuple(params))
    offres = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return {"offres": offres}

@app.get("/offres/{offre_id}")
def get_offre(offre_id: int):
    """ Récupère une offre spécifique par son ID """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM offres WHERE id = %s", (offre_id,))
    offre = cursor.fetchone()

    cursor.close()
    conn.close()

    if not offre:
        return {"message": "Offre non trouvée"}

    return offre

# 🔹 Démarrer l'API pour Cloud Run (Uvicorn)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Cloud Run fournit ce port dynamiquement
    uvicorn.run(app, host="0.0.0.0", port=port)
