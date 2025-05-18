CREATE TABLE offres (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(255),
    contrat VARCHAR(100),
    lieu VARCHAR(100),
    lien VARCHAR(500),
    description TEXT,
    datescraping DATE DEFAULT CURRENT_DATE,
    ville VARCHAR(100),
    dateoffre DATE,
    nomclient VARCHAR(255),
    logo VARCHAR(500),
    secteur VARCHAR(100),
    teletravail VARCHAR(50),
    salaire VARCHAR(100),
    groupeparent VARCHAR(255)
);
