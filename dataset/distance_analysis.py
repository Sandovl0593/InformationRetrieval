#despues de ejecutar el script "extract_features.py" ejecutar este script "distance_analysis" <- (1)
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(eval(mfcc_string))

# Función para calcular la distancia euclidiana
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Función para limpiar nombres de canciones eliminando caracteres problemáticos
def clean_song_name(song_name):
    return re.sub(r'[^\w\s]', '', song_name)

# Cargar datos
df = pd.read_csv('complete_spotify_with_mfcc.csv')

# Verificar la estructura de los datos en MFCC_Vector antes de la conversión
print("Estructura de datos en MFCC_Vector antes de la conversión:")
print(df['MFCC_Vector'].head())

# Convertir la columna MFCC_Vector en arrays de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)

# Verificar la estructura de los datos después de la conversión
print("\nEstructura de datos en MFCC_Vector después de la conversión:")
print(df['MFCC_Vector'].head())

# Vector de consulta
query_vector = df.iloc[11391]['MFCC_Vector']
query_song_name = df.iloc[11391]['track_name']
query_artist_name = df.iloc[11391]['track_artist']

# Calcular distancias
distances = []
song_names = []

for index, row in df.iterrows():
    distance = euclidean_distance(query_vector, row['MFCC_Vector'])
    distances.append(distance)
    song_name = f"{row['track_name']} by {row['track_artist']}"
    cleaned_song_name = clean_song_name(song_name)
    song_names.append(cleaned_song_name)

# Imprimir distancias con nombres de canciones
for name, dist in zip(song_names, distances):
    print(f"Distancia con {name}: {dist}")

# Para visualizar distancias
plt.figure(figsize=(10, 6))

# Graficando solo las primeras 5 canciones para mejor visibilidad
plt.bar(song_names[:5], distances[:5])
plt.xlabel('Songs')
plt.ylabel('Distance')
plt.title(f'Distance Distribution from "{query_song_name}" by {query_artist_name}')
plt.xticks(rotation=45, ha="right")
plt.subplots_adjust(bottom=0.3)

plt.tight_layout()
plt.show()
