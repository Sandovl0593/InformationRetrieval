-- Crear la tabla
CREATE TABLE tracks (
    track_id VARCHAR,
    track_name VARCHAR,
    track_artist VARCHAR,
    lyrics TEXT,
    track_popularity INTEGER,
    track_album_id VARCHAR,
    track_album_name VARCHAR,
    track_album_release_date VARCHAR, 
    playlist_name VARCHAR,
    playlist_id VARCHAR,
    playlist_genre VARCHAR,
    playlist_subgenre VARCHAR,
    danceability NUMERIC,
    energy NUMERIC,
    key INTEGER,
    loudness NUMERIC,
    mode INTEGER,
    speechiness NUMERIC,
    acousticness NUMERIC,
    instrumentalness NUMERIC,
    liveness NUMERIC,
    valence NUMERIC,
    tempo NUMERIC,
    duration_ms INTEGER,
    language VARCHAR,
    text TEXT,
    tokens TEXT,
    filtered_tokens TEXT,
    stemmed_tokens TEXT
);

COPY tracks FROM '/Users/fernandoguill3n/data.csv' DELIMITER '@' CSV HEADER;

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Creación de la columna tsvector

ALTER TABLE tracks ADD COLUMN tsvector_col tsvector;
-- Actualización de la columna tsvector

UPDATE tracks SET tsvector_col = to_tsvector('spanish', unaccent(contenido_textual));

-- Creación del índice GIN
CREATE INDEX idx_tsvector ON tracks USING GIN(tsvector_col);

-- Consulta con similitud de coseno
SELECT id, contenido_textual, ts_rank_cd(tsvector_col, query) AS rank
FROM tracks, to_tsquery('ejemplo', 'ejemplo') AS query
WHERE tsvector_col @@ query
ORDER BY rank DESC
LIMIT 10;