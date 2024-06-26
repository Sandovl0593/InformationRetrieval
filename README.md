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
El objetivo principal de esta primera parte del proyecto es construir un sistema de búsqueda y recuperación de información eficiente y efectivo utilizando un índice invertido para documentos de texto. Este índice invertido permitirá realizar búsquedas rápidas y precisas sobre una colección de datos textuales de gran tamaño. La construcción del índice incluye el preprocesamiento de datos, la tokenización, el filtrado de stopwords, y la reducción de palabras mediante stemming. Al culminar esta primera fase con éxito, se establecerá una base sólida para la segunda parte del proyecto, que se enfocará en la implementación de una estructura multidimensional para la búsqueda eficiente de imágenes y audio, optimizando así un sistema de recomendación integral.

### Descripción del dominio de datos y la importancia de aplicar indexación.
El dominio de datos utilizado en este proyecto consiste en un conjunto de canciones de Spotify, que incluye información tanto textual como no textual. Los campos textuales incluyen el nombre de la pista, el artista, las letras, el nombre del álbum, el nombre de la lista de reproducción, el género, el subgénero y el idioma. Los campos no textuales incluyen métricas como la popularidad de la pista, el ID del álbum, la fecha de lanzamiento del álbum, el ID de la lista de reproducción, así como características de audio como la capacidad de baile, la energía, la clave, la sonoridad, el modo, la habla, la acústica, la instrumentalidad, la vivacidad, la valencia, el tempo y la duración en milisegundos.

La indexación es crucial en este contexto debido a la gran cantidad de datos textuales y la necesidad de realizar búsquedas eficientes y precisas. Sin un índice adecuado, buscar información relevante en un gran volumen de datos sería extremadamente lento y poco práctico. El uso de un índice invertido permite acceder rápidamente a los documentos que contienen los términos de consulta, mejorando significativamente el rendimiento de las búsquedas y proporcionando resultados más precisos. Además, la indexación nos ayuda a gestionar y consultar de manera eficiente los datos textuales, permitiendo realizar búsquedas precisas basadas en el campo "text", que es la concatenación de todos los campos textuales. Esto mejora la relevancia y precisión de los resultados de búsqueda al enfocarse en el contenido textual de las canciones.

## Backend
### Preprocesamiento
El preprocesamiento es una etapa clave en la construcción de nuestro índice invertido porque permite normalizar y limpiar los datos textuales, asegurando que el proceso de indexación sea eficiente y los resultados de búsqueda sean precisos y relevantes. Al transformar el texto en una forma más manejable y consistente, se mejora la capacidad del sistema para identificar y recuperar información pertinente. En este proyecto, se llevaron a cabo los siguientes pasos para nuestro preprocesamiento:

1) Concatenación de Campos Textuales: Se concatenaron todos los campos textuales relevantes en un solo texto por fila, utilizando el carácter especial "@" como delimitador para evitar conflictos con comas presentes en las letras de las canciones. Esto incluye campos como el nombre de la pista, el artista, las letras, el nombre del álbum, el nombre de la lista de reproducción, el género, el subgénero y el idioma. La columna resultante, denominada "text", contiene estos datos combinados para cada fila del dataset.


2) Tokenización: El texto concatenado se dividió en palabras individuales o tokens. Este paso es crucial para analizar y procesar cada palabra de manera independiente. La columna resultante, denominada "tokens", contiene una lista de palabras extraídas del texto concatenado.


3) Filtrado de Stopwords: Se eliminaron las palabras comunes y de poco valor semántico conocidas como stopwords (por ejemplo, "el", "la", "de"). Esto ayuda a reducir el ruido en los datos y enfocar el análisis en las palabras más significativas. La columna resultante, denominada "filtered_tokens", contiene la lista de palabras después de eliminar las stopwords.


4) Stemming: Se aplicó un algoritmo de stemming para reducir las palabras a su raíz o forma básica. Por ejemplo, las palabras "correr", "corriendo" y "corrí" se reducen a la raíz común "corr". Esto ayuda a unificar las diferentes formas de una palabra y mejora la relevancia de las búsquedas. La columna resultante, denominada "stemmed_tokens", contiene las palabras después de aplicar el stemming.

Resumen del Proceso Completo de Preprocesamiento:

- Concatenación de Campos Textuales: Se combinan los valores de los campos textuales en una sola cadena para cada fila del dataset.


- Tokenización: Se divide el texto concatenado en palabras individuales, creando una lista de tokens.


- Filtrado de Stopwords: Se eliminan las palabras comunes que no aportan mucho significado para el análisis.


- Stemming: Se reduce cada palabra a su raíz o forma base, lo que ayuda a normalizar las palabras y reducir la dimensionalidad del texto.

### Índice Invertido

- Construcción del índice invertido en memoria secundaria:
    
    El índice invertido es fundamental para asegurar búsquedas eficientes y rápidas en grandes volúmenes de datos textuales. Para construir el índice invertido en memoria secundaria, realizamos los siguientes estos pasos:
    1) Extracción de la Columna Relevante (text):

        Antes de construir el índice invertido, es importante aclarar que extragimos solo la columna relevante del dataset que contiene el texto preprocesado. Para ello, se utiliza el script test.py, el cual se encarga de generar un archivo text.csv con la columna "text". Este paso garantiza que el índice no cargue toda la data, sino únicamente la información esencial (relevante) para las búsquedas textuales.
  2) Construcción del Índice:

     1. Tokenización y Cálculo de TF-IDF
     Cada documento es tokenizado, y se calcula el TF-IDF (Term Frequency-Inverse Document Frequency) para cada término en el documento. Este paso pondera la importancia de cada término dentro de un documento y en el corpus completo.

     2. Estructuración del Índice
     Los términos tokenizados y sus respectivas ponderaciones TF-IDF se almacenan en una estructura de datos adecuada para consultas eficientes. Esta estructura se guarda en memoria secundaria para manejar grandes volúmenes de datos.

     3. Algoritmo SPIMI (Single-pass In-memory Indexing)
     
        El algoritmo SPIMI es utilizado para la construcción del índice invertido en bloques, permitiendo manejar grandes volúmenes de datos sin necesidad de mucha memoria.
    
     - Pasos del Algoritmo SPIMI:
    
        Procesamiento del Flujo de Tokens: Se procesa el flujo de tokens, contando la frecuencia de términos (term_freq).
        Construcción del Diccionario: Se construye un diccionario donde cada término apunta a una lista de postings (documentos y frecuencias).
        Escritura en Disco: Los postings se escriben a archivos temporales para manejar grandes volúmenes de datos sin sobrecargar la memoria.
        Puntos Fuertes de SPIMI:
        
     - Eficiencia de Memoria: Al escribir bloques a disco, SPIMI maneja eficientemente grandes volúmenes de datos sin necesitar mucha memoria.
     - Simplicidad: Es relativamente sencillo de implementar y entender.
        
- Ejecución óptima de consultas aplicando Similitud de Coseno

    Una vez construido el índice invertido, las consultas se ejecutan aplicando la similitud de coseno entre el vector de la consulta y los vectores de los documentos indexados. Este proceso incluye los siguientes pasos:
    
    1) Vectorización de la Consulta: La consulta ingresada por el usuario se tokeniza y se convierte en un vector de términos.
    2) Cálculo de Similitud: Se calcula la similitud de coseno entre el vector de la consulta y los vectores de los documentos en el índice. Esto implica utilizar los pesos TF-IDF previamente calculados y las normas de los documentos almacenadas.
    3) Rankeo de Resultados: Los documentos se ordenan según su similitud con la consulta, y se retorna el top-k de documentos más relevantes.


- Explique cómo se construye el índice invertido en
PostgreSQL 

  El sistema utiliza PostgreSQL para almacenar y recuperar textos mediante índices optimizados y funciones de similitud avanzadas. A continuación se detallan los pasos clave y tecnologías utilizadas:

  - Configuración Inicial y Carga de Datos 
    
    Se creó una tabla `songs` para almacenar datos relacionados con canciones, incluyendo un campo `text` para las letras de las canciones. Los datos se cargaron desde un archivo CSV.

  - Uso de Extensiones PostgreSQL

    Se instalaron y configuraron las extensiones `pg_trgm` y `unaccent` para mejorar las capacidades de búsqueda.

  - Creación de Columna y Índice

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


## Frontend


### 1) Diseño de la GUI
Nuestro frontend permite a los usuarios interactuar con el índice invertido y realizar búsquedas de manera sencilla y eficiente. A continuación, se describen los componentes principales de la GUI y su funcionamiento:

- Mini-manual de usuario

    - Ingreso de Consulta: El usuario puede ingresar una frase en lenguaje natural en el campo de búsqueda.
    - Selección de Top-K Resultados: El usuario puede especificar cuántos documentos (Top K) desea recuperar.
    - Ejecución de Búsqueda: Al presionar el botón de "Consultar"", el sistema procesa la consulta y muestra los resultados.
    - Visualización de Resultados: Los resultados se presentan de manera amigable, indicando el tiempo de procesamiento de la consulta.
    - Selección del Método de Indexación: El usuario puede elegir entre nuestra propia implementación del índice invertido o el uso de bases de datos PostgreSQL para realizar la búsqueda.

- Screenshots de la GUI
    - Pantalla de Inicio:
    
      Al ingresar a la interfaz gráfica, se puede observar que la pantalla inicial cuenta con varios campos importantes. Estos incluyen un campo para ingresar la consulta textual que se desea buscar, una opción para seleccionar el Top K resultados, y un selector para elegir la técnica de indexación (Manual o PostgreSQL). Además, el usuario puede especificar la cantidad de datos sobre los cuales desea realizar la búsqueda, con opciones de 1000, 5000, 10000, 15000, o Todos.

    ![Pantalla de Inicio](images/6.png)

    - Resultados de Búsqueda:
     
     Como se puede observar en la imagen a continuación, estamos buscando una canción que contenga la palabra "Hola", utilizando la técnica "Manual", con un Top K de 25 y una cantidad de datos de 1000.
    ![Pantalla de Inicio](images/5.png)

     Hemos encontrado una coincidencia para la consulta realizada con la palabra "Hola". La canción encontrada se llama "Me Enamoré" del artista "Jhay Wheeler", como se puede observar en la imagen a continuación.

    ![Pantalla de Inicio](images/4.png)
     En la siguiente imagen, podemos ver que el tiempo de ejecución de esta consulta fue de "898.0598 ms".

    ![Pantalla de Inicio](images/3.png)
     Por último, en la última imagen podemos confirmar que la letra de la canción "Me Enamoré" del artista Jhay Wheeler efectivamente contiene la palabra "Hola", tal y como se buscó.

    ![Pantalla de Inicio](images/2.png)

### 2) Análisis comparativo visual con otras implementaciones
#### MyIndex Vs PostgreSQL:
- My Index:
Como podemos observar, al implementar la tecnica Manual (MyIndex) el tiempo de ejecución para procesar la consulta "Hola" fue de "898.0598 ms".
    ![Pantalla de Inicio](images/5.png)
    ![Pantalla de Inicio](images/4.png)
    ![Pantalla de Inicio](images/3.png)
    ![Pantalla de Inicio](images/2.png)



## Experimentación

### PostgreSQL
#### Grafica Obtenida:
![Pantalla de Inicio](images/1.png)


Basado en los resultados de la experimentación con PostgreSQL para la búsqueda del término "Toxica" en diferentes tamaños de bases de datos (1000, 5000, 10000, 15000 registros y todos los registros disponibles), podemos obtener las siguientes conclusiones:

Rendimiento Consistente: En general, los tiempos de ejecución se mantienen relativamente estables a medida que aumenta el tamaño de la base de datos. Esto sugiere que PostgreSQL maneja eficientemente las consultas de búsqueda de texto completo utilizando índices GIN y funciones de similitud como ts_rank_cd.

Escalabilidad: El sistema muestra una buena escalabilidad, ya que no se observa un aumento significativo en el tiempo de ejecución a medida que se añaden más registros. Esto es una ventaja cuando se trata de manejar grandes volúmenes de datos y proporciona una experiencia de usuario consistente independientemente del tamaño de la base de datos.

Optimización de Consultas: La utilización de índices GIN en la columna tsvector_col y la aplicación de la función to_tsvector para procesar los textos parecen ser efectivas para optimizar las consultas de búsqueda. Esto se refleja en los tiempos de ejecución relativamente bajos incluso para bases de datos más grandes.

Consultas Repetidas: Cuando ejecutas la misma consulta varias veces, PostgreSQL puede aprovechar la caché para devolver resultados más rápidamente en las ejecuciones posteriores. Esto puede hacer que los tiempos de respuesta aparenten ser más rápidos de lo que serían en condiciones de caché vacía.

## Conclusiones

En resumen para la experimentacion con PostgreSQL, los resultados indican que es una opción robusta para implementar sistemas de recuperación de información basados en texto, proporcionando buen rendimiento y escalabilidad. Sin embargo, siempre es importante monitorear y ajustar según las cargas de trabajo y requisitos específicos del proyecto para garantizar un rendimiento óptimo a largo plazo.



### MyIndex VS PostgreSQL
![Pantalla de Inicio](images/graficaaaaa.jpg)
Inicialmente, ambas técnicas tienen tiempos de ejecución similares. Sin embargo, a medida que aumenta la cantidad de datos, la técnica del Índice Invertido que hemos implementado empieza a mostrar una mejora significativa en comparación con PostgreSQL, especialmente en rangos de datos entre 1000 y 10,000. En este intervalo, se observa una clara ventaja en los tiempos de nuestro Índice Invertido. Aunque al final los tiempos totales van parecidas o muy cercanos entre sí, podemos concluir que el Índice Invertido es más eficiente en conjuntos de datos relativamente grandes. No obstante, cuando la cantidad de datos sigue creciendo, nuestro índice muestra un aumento y llega a un pico en los tiempos de ejecución alrededor de los 15,000 datos. Finalmente, al llegar a cantidades de datos aún mayores, como el "TOTAL" mostrado en la gráfica, los tiempos de ejecución del Índice Invertido se regulan y vuelven a disminuir, demostrando una mejora en comparación con el pico observado anteriormente y presentando inclusive en ese momento en el que se tiende al "TOTAL" de datos, un mejor tiempo en comparación al de PostgreSQL.


## Pasos para ejecutar el proyecto:

Sigue estos pasos para configurar y ejecutar correctamente el proyecto.

### 1. Preparación inicial

#### 1.1. Clona el repositorio

Primero, clona el repositorio desde GitHub:

```
git clone https://github.com/Sandovl0593/InformationRetrieval.git
cd InformationRetrieval
```
### 2. Configuración del entorno virtual y dependencias
#### 2.1. Crea un entorno virtual
Crea un entorno virtual para aislar las dependencias del proyecto:
```
python -m venv venv
```
#### 2.2. Activa el entorno virtual
En Windows, activa el entorno virtual con:

```
venv\Scripts\activate
```

En macOS/Linux, usa:

```
source venv/bin/activate
```

#### 2.3. Instala las dependencias
Instala las dependencias necesarias desde el archivo "requirements.txt":

```
pip install -r requirements.txt
```

### 3. Descarga y preparación del dataset

#### 3.1. Descarga el dataset desde Kaggle

Descarga el dataset [spotify_songs.csv](https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs?select=spotify_songs.csv) de la plataforma Kaggle.


Asegúrate de colocar el archivo descargado spotify_songs.csv en la carpeta "dataset" de tu proyecto.

### 4. Ejecución de scripts de preparación de datos
#### 4.1. Ejecuta el script de preprocesamiento de texto
Primero, ejecuta el script textpreprocessor.py en la carpeta dataset para procesar los datos:

```
python dataset/textpreprocessor.py
```
#### 4.2. Ejecuta el script principal para generar archivos reducidos
Luego, ejecuta el script text.py en la carpeta dataset para generar archivos reducidos:

```
python dataset/text.py
```
### 5. Iniciar el servidor Flask
#### 5.1. Configura el entorno Flask
Asegúrate de que el archivo .flaskenv tenga las siguientes líneas:

```
FLASK_APP=server.py
FLASK_DEBUG=1
```

#### 5.2. Ejecuta el servidor Flask
Finalmente, inicia el servidor Flask ejecutando el siguiente comando:

```
flask run
```

Esto iniciará el servidor correctamente y te proporcionará el enlace donde podrás acceder e interactuar con el proyecto.
