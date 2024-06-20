<a name="readme-top"></a>

<div align="center">
  <a href="https://https://github.com/Sandovl0593/InformationRetrieval">
  </a>
  <h1>Information Retrieval</h1>
</div>
<h3 align="center">Base de Datos II - Proyecto 02</h3>

## Integrantes

- Espinoza Herrera, Marcela
- Sandoval Huamaní, Adrian
- Guillén Rodriguez, Fernando
- Lindo Peña, Ximena Nicolle

## Introducción

### Objetivo del Proyecto

### Descripción del Dominio de Datos

## Índice Invertido

### Preprocesamiento

### Construcción

### Optimización con SPIMI


## Indice con PostgreSQL


El sistema utiliza PostgreSQL para almacenar y recuperar textos mediante índices optimizados y funciones de similitud avanzadas. A continuación se detallan los pasos clave y tecnologías utilizadas:

### Configuración Inicial y Carga de Datos

Se creó una tabla `songs` para almacenar datos relacionados con canciones, incluyendo un campo `text` para las letras de las canciones. Los datos se cargaron desde un archivo CSV.

### Uso de Extensiones PostgreSQL

Se instalaron y configuraron las extensiones `pg_trgm` y `unaccent` para mejorar las capacidades de búsqueda.

### Creación de Columna y Índice

Se agregó una columna `tsvector_col` de tipo `tsvector` y se creó un índice GIN en esta columna para optimizar las consultas de búsqueda de texto completo.


```sql
ALTER TABLE songs ADD COLUMN tsvector_col tsvector;
UPDATE songs SET tsvector_col = to_tsvector('spanish', unaccent(text));
CREATE INDEX idx_tsvector ON songs USING GIN(tsvector_col);
```

Se utilizó la función ts_rank_cd para calcular la similitud de coseno entre el contenido del tsvector_col y una consulta de texto representada por to_tsquery.
```sql
SELECT track_id, track_name, track_artist,
       ts_rank_cd(tsvector_col, query) AS rank
FROM songs, to_tsquery('spanish', 'gola') AS query
WHERE tsvector_col @@ query
ORDER BY rank DESC;
```

## Experimentación

### Implementación propia

### PostgreSQL

## Conclusiones
