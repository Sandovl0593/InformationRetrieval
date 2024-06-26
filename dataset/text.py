import random as rd
import pandas as pd

class TextExtractor:
    def __init__(self, input_filepath):
        self.input_filepath = input_filepath

    def extract_text_column(self, output_filepath, num_rows=None):
        # Leer el archivo CSV procesado
        data = pd.read_csv(self.input_filepath, sep='@', encoding='utf-8')

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
output_filepath_sample = 'document_songs.csv'
extractor.extract_text_column(output_filepath_sample)

print(f"Las filas la columna 'text' han sido extraídas y guardadas en {output_filepath_sample}")

with open(output_filepath_sample, encoding="utf-8", mode="r") as f:
    # select N random rows
    content = [line[1:-1] for line in f.readlines()[1:]]

for i in [500, 1000, 5000, 10000, 15000]:
    sampled_df = pd.DataFrame(content[:i+1], columns=['text'])
    output_filepath = f'songs_reduced_{i}.csv'
    sampled_df.to_csv(output_filepath, index=False, sep='@', encoding='utf-8')

print("Archivos generados en distintos tamaños de filas.")