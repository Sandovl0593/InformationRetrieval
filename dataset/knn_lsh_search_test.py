import pandas as pd
import numpy as np
import re
import ast
from heapq import heappush, heappop

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(ast.literal_eval(mfcc_string))

# Función hash basada en proyecciones aleatorias
def hash_function(vector, random_vectors):
    return tuple((vector.dot(random_vector) > 0).astype(int) for random_vector in random_vectors)

# Crear el índice LSH
def create_lsh_index(data, num_hash_functions, vector_size):
    random_vectors = [np.random.randn(vector_size) for _ in range(num_hash_functions)]
    lsh_index = {}
    
    for index, row in data.iterrows():
        mfcc_vector = row['MFCC_Vector']
        hash_value = hash_function(mfcc_vector, random_vectors)
        if hash_value not in lsh_index:
            lsh_index[hash_value] = []
        lsh_index[hash_value].append((index, mfcc_vector))
    
    return lsh_index, random_vectors

# Búsqueda KNN usando LSH
def lsh_knn_search(query_vector, lsh_index, random_vectors, K):
    query_hash = hash_function(query_vector, random_vectors)
    candidate_vectors = lsh_index.get(query_hash, [])
    
    if len(candidate_vectors) == 0:
        return []

    distances = []
    for index, vector in candidate_vectors:
        distance = np.linalg.norm(query_vector - vector)
        distances.append((distance, index))
    
    distances.sort()
    return distances[:K]

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

# Crear el índice LSH
num_hash_functions = 2 # Ajustar este valor dependiendo de la dimension del dataset (A mayor dimension mayor num_hash_funcitons)
vector_size = len(query_vector)
lsh_index, random_vectors = create_lsh_index(df, num_hash_functions, vector_size)

# Buscar los K vecinos más cercanos usando LSH
K = 3
neighbors = lsh_knn_search(query_vector, lsh_index, random_vectors, K)

# Imprimiendo resultados
for distance, index in neighbors:
    track_info = df.iloc[index]
    print(f"Distance: {distance}, Track: {track_info['track_name']}, Artist: {track_info['track_artist']}")
