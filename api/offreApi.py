from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor
import os

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
    """ etablit une connexion PostgreSQL """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.get("/")
def read_root():
    return {"message": "API de gestion des offres d'emploi"}

@app.get("/offres")
def get_offres(
    contrat: str = Query(None),
    ville: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Recupere les offres avec filtres + pagination (20 offres par defaut par page).
    """
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

    query += " ORDER BY dateoffre DESC "

    # Pagination
    offset = (page - 1) * limit
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    offres = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "page": page,
        "limit": limit,
        "results": len(offres),
        "offres": offres
    }

@app.get("/offres/{offre_id}")
def get_offre(offre_id: int):
    """ Recupere une offre specifique par son ID """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM offres WHERE id = %s", (offre_id,))
    offre = cursor.fetchone()

    cursor.close()
    conn.close()

    if not offre:
        return {"message": "Offre non trouvee"}

    return offre

# 🔹 Pour execution locale (utile pour debug)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
