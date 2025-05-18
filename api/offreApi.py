from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# 🔹 CORS
origins = [
    "https://horsesn.fr",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Connexion PostgreSQL
DB_CONFIG = {
    "host": "/cloudsql/horsesn:us-central1:offres",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.get("/")
def read_root():
    return {"message": "API de gestion des offres d'emploi"}

@app.get("/offres")
def get_offres(
    contrat: str = Query(None),
    ville: str = Query(None),
    secteur: str = Query(None),
    teletravail: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    params = []
    where_clauses = ["1=1"]

    if search:
        phrase = f"%{search.strip()}%"
        words = search.strip().split()

        # Phrase exacte d'abord
        priority_case = """
            CASE
                WHEN nomclient ILIKE %s THEN 4
                WHEN titre ILIKE %s THEN 4
        """
        params += [phrase, phrase]

        # Puis tous les mots (en AND)
        for w in words:
            priority_case += f"""
                WHEN nomclient ILIKE %s THEN 3
            """
            params.append(f"%{w}%")
        for w in words:
            priority_case += f"""
                WHEN titre ILIKE %s THEN 2
            """
            params.append(f"%{w}%")
        for w in words:
            priority_case += f"""
                WHEN description ILIKE %s THEN 1
            """
            params.append(f"%{w}%")

        priority_case += " ELSE 0 END AS priority"

        # WHERE clause : tous les mots dans n'importe quel champ
        search_conditions = []
        for w in words:
            w_like = f"%{w}%"
            search_conditions += [
                "nomclient ILIKE %s",
                "titre ILIKE %s",
                "description ILIKE %s"
            ]
            params += [w_like, w_like, w_like]

        where_clause = " OR ".join(search_conditions)

        query = f"""
            SELECT *, {priority_case}
            FROM offres
            WHERE ({where_clause})
        """
    else:
        query = "SELECT *, 0 AS priority FROM offres WHERE 1=1"

    # Filtres additionnels
    if contrat:
        query += " AND contrat = %s"
        params.append(contrat)
    if ville:
        query += " AND ville = %s"
        params.append(ville)
    if secteur:
        query += " AND secteur = %s"
        params.append(secteur)
    if teletravail:
        query += " AND teletravail = %s"
        params.append(teletravail)

    # Tri
    if search:
        query += " ORDER BY priority DESC, dateoffre DESC"
    else:
        query += " ORDER BY dateoffre DESC, RANDOM()"

    # Pagination
    offset = (page - 1) * limit
    query += " LIMIT %s OFFSET %s"
    params += [limit, offset]

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
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM offres WHERE id = %s", (offre_id,))
    offre = cursor.fetchone()

    cursor.close()
    conn.close()

    if not offre:
        return {"message": "Offre non trouvée"}
    return offre

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
