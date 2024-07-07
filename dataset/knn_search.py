# Luego de ejecutar el "distance_analysis.py" ejecutar el "knn_search.py" <- (2)
import pandas as pd
import numpy as np
from heapq import heappush, heappop
import ast  # Para una conversión segura de strings a listas
import re

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(ast.literal_eval(mfcc_string))

# Función para calcular la distancia euclidiana
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Busqueda KNN con cola de prioridad
def knn_search(query_vector, data, K):
    priority_queue = []
    for index, row in data.iterrows():
        distance = euclidean_distance(query_vector, row['MFCC_Vector'])
        heappush(priority_queue, (-distance, (index, row)))  # Usar distancia negativa para heappop más cercano
        if len(priority_queue) > K:
            heappop(priority_queue)

    # Recolectar y retornar los K vecinos más cercanos
    neighbors = []
    while priority_queue:
        neighbors.append(heappop(priority_queue))
    return neighbors[::-1]

# Cargar datos
df = pd.read_csv('complete_spotify_with_mfcc.csv')

# Convertir MFCC_Vector de cadena a array de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)

# Vector de consulta
query_vector = df.iloc[11391]['MFCC_Vector']

# Validación de las estructuras de todos los vectores MFCC
for index, row in df.iterrows():
    vector = row['MFCC_Vector']
    if vector.shape != query_vector.shape:
        print(f"Row {index} has a vector of different shape: {vector.shape}")

# Buscar los K vecinos más cercanos
K = 3
neighbors = knn_search(query_vector, df, K)

# Imprimiendo resultados
for neg_dist, (index, neighbor) in neighbors:
    dist = -neg_dist  # Reconvertir la distancia a positiva
    print(f"Distance: {dist}, Track: {neighbor['track_name']}, Artist: {neighbor['track_artist']}")
