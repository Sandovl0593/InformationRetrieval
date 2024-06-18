import pandas as pd

class TextExtractor:
    def __init__(self, input_filepath):
        self.input_filepath = input_filepath

    def extract_text_column(self, output_filepath, num_rows=None):
        # Leer el archivo CSV procesado
        data = pd.read_csv(self.input_filepath, sep='@')

        # Extraer la columna 'text'
        text_data = data[['text']]

        # Si se especifica num_rows, seleccionar las primeras num_rows filas
        if num_rows is not None:
            text_data = text_data.head(num_rows)

        # Guardar la columna 'text' en un nuevo archivo CSV
        text_data.to_csv(output_filepath, index=False, sep='@')


input_filepath = 'spotify_songs_procesado.csv'

# Para generar el archivo completo (con todas las filas de text):
#output_filepath_full = 'text.csv'
extractor = TextExtractor(input_filepath)
#extractor.extract_text_column(output_filepath_full)
#print(f"La columna 'text' completa ha sido extraída y guardada en {output_filepath_full}")

# Para generar un archivo con solo las 3 primeras filas de text:
output_filepath_sample = 'text_3filas.csv'
extractor.extract_text_column(output_filepath_sample, num_rows=3)
print(f"Las primeras 3 filas de la columna 'text' han sido extraídas y guardadas en {output_filepath_sample}")
