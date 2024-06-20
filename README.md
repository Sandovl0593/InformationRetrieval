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
Basado en los resultados de la experimentación con PostgreSQL para la búsqueda del término "Toxica" en diferentes tamaños de bases de datos (1000, 5000, 10000, 15000 registros y todos los registros disponibles), podemos obtener las siguientes conclusiones:

Rendimiento Consistente: En general, los tiempos de ejecución se mantienen relativamente estables a medida que aumenta el tamaño de la base de datos. Esto sugiere que PostgreSQL maneja eficientemente las consultas de búsqueda de texto completo utilizando índices GIN y funciones de similitud como ts_rank_cd.

Escalabilidad: El sistema muestra una buena escalabilidad, ya que no se observa un aumento significativo en el tiempo de ejecución a medida que se añaden más registros. Esto es una ventaja cuando se trata de manejar grandes volúmenes de datos y proporciona una experiencia de usuario consistente independientemente del tamaño de la base de datos.

Optimización de Consultas: La utilización de índices GIN en la columna tsvector_col y la aplicación de la función to_tsvector para procesar los textos parecen ser efectivas para optimizar las consultas de búsqueda. Esto se refleja en los tiempos de ejecución relativamente bajos incluso para bases de datos más grandes.

Consultas Repetidas: Cuando ejecutas la misma consulta varias veces, PostgreSQL puede aprovechar la caché para devolver resultados más rápidamente en las ejecuciones posteriores. Esto puede hacer que los tiempos de respuesta aparenten ser más rápidos de lo que serían en condiciones de caché vacía.

## Conclusiones

En resumen para la experimentacion con PostgreSQL, los resultados indican que es una opción robusta para implementar sistemas de recuperación de información basados en texto, proporcionando buen rendimiento y escalabilidad. Sin embargo, siempre es importante monitorear y ajustar según las cargas de trabajo y requisitos específicos del proyecto para garantizar un rendimiento óptimo a largo plazo.
