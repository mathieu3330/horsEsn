from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware # <-- Ajout de l'import
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# 🔹 Configuration CORS
origins = [
    "https://horsesn.fr",
    "http://localhost:5173"
    # Ajoutez d'autres origines si nécessaire (ex: http://localhost:xxxx pour le dev) 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # <-- Ajout du middleware CORS

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
    Recupere les offres avec filtres + pagination.
    Affiche par dateoffre descendante puis random léger pour mélanger légèrement les offres.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        query = """
            SELECT *, ts_rank_cd(to_tsvector('french', titre || ' ' || description), plainto_tsquery('french', %s)) AS rank
            FROM offres
            WHERE to_tsvector('french', titre || ' ' || description) @@ plainto_tsquery('french', %s)
        """
        params = [search, search]
    else:
        query = "SELECT * FROM offres WHERE 1=1"
        params = []

    if contrat:
        query += " AND contrat = %s"
        params.append(contrat)
    if ville:
        query += " AND ville = %s"
        params.append(ville)

    if search:
        query += " ORDER BY rank DESC, dateoffre DESC"   # Si recherche : par score puis par dateoffre
    else:
        query += " ORDER BY dateoffre DESC, RANDOM()"     # Si pas de recherche : dateoffre récente + mélange léger

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

