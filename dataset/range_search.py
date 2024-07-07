# Y despues de haber ejecutado el "knn_search.py" ejecutar el "range_search.py" <- (3)
import pandas as pd
import numpy as np
import ast  # Para una conversión segura de strings a listas
import re
import matplotlib.pyplot as plt

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(ast.literal_eval(mfcc_string))

# Función para calcular la distancia euclidiana
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Busqueda por rango
def range_search(query_vector, data, radius, sort_results=True):
    results = []
    for index, row in data.iterrows():
        distance = euclidean_distance(query_vector, row['MFCC_Vector'])
        if distance <= radius:
            results.append((distance, row))
    # Ordenar los resultados por distancia si sort_results es True
    if sort_results:
        results.sort(key=lambda x: x[0])
    return results

# Cargar datos
df = pd.read_csv('complete_spotify_with_mfcc.csv')

# Convertir MFCC_Vector de cadena a array de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)

# Vector de consulta (puede ser la primera canción como en el ejemplo)
query_vector = df.iloc[11391]['MFCC_Vector']

# Radios de búsqueda
radii = [16.0, 18.8, 20.0]

for radius in radii:
    print(f"\nResultados para radio = {radius}:")
    results_within_radius = range_search(query_vector, df, radius)
    for dist, result in results_within_radius:
        print(f"Distance: {dist}, Track: {result['track_name']}, Artist: {result['track_artist']}")

    # Analisis de la distribución de la distancia
    distances = [dist for dist, _ in results_within_radius]
    tracks = [result['track_name'] for _, result in results_within_radius]
    print(f"Distancias para radio = {radius}: {distances}")

    # Verificar que estamos incluyendo todas las distancias
    print(f"Número de canciones dentro del radio {radius}: {len(distances)}")

    # Graficando histograma de la distribución de distancias
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(len(distances)), distances, tick_label=tracks, edgecolor='black')
    plt.xlabel('Track')
    plt.ylabel('Distance')
    plt.title(f'Distance Distribution for Radius = {radius}')
    plt.xticks(rotation=45, ha='right')

    # Añadiendo etiquetas a las barras
    for bar, dist in zip(bars, distances):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(dist, 2), va='bottom')  # Etiqueta con la distancia

    plt.show()
