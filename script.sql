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
    stemmed_tokens TEXT,
    tsvector_col tsvector  -- Columna para índice de texto completo
);

-- Cargar datos desde CSV con delimitador '@'
COPY tracks FROM '/Users/fernandoguill3n/data.csv' DELIMITER '@' CSV HEADER;

-- Crear extensiones necesarias si no están instaladas
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Extension para trigramas
CREATE EXTENSION IF NOT EXISTS unaccent; -- Extension para remover acentos

-- Crear la columna tsvector
ALTER TABLE tracks ADD COLUMN tsvector_col tsvector;

-- Actualizar la columna tsvector con el texto procesado
UPDATE tracks SET tsvector_col = to_tsvector('spanish', unaccent(text));

-- Crear el índice GIN en tsvector_col para optimizar búsquedas de texto completo
CREATE INDEX idx_tsvector ON tracks USING GIN(tsvector_col);

-- Consulta con similitud de coseno
SELECT track_id, track_name, track_artist,
       ts_rank_cd(tsvector_col, query) AS rank
FROM tracks, to_tsquery('spanish', 'consulta de ejemplo') AS query
WHERE tsvector_col @@ query
ORDER BY rank DESC;
