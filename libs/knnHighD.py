import numpy as np
import re
import ast
from collections import defaultdict
from scipy.spatial.distance import euclidean

# Función hash basada en proyecciones aleatorias
def hash_function(vector, random_vectors):
    return tuple((vector.dot(random_vector) > 0).astype(int) for random_vector in random_vectors)

# Crear el índice LSH
def create_lsh_index(data, num_hash_functions, vector_size):
    random_vectors = [np.random.randn(vector_size) for _ in range(num_hash_functions)]
    lsh_index = defaultdict(list)
    
    for index, row in data.iterrows():
        mfcc_vector = row['MFCC_Vector']
        hash_value = hash_function(mfcc_vector, random_vectors)
        lsh_index[hash_value].append((index, mfcc_vector))
    
    return lsh_index, random_vectors

# Búsqueda KNN usando LSH
def lsh_knn_search(query_vector, lsh_index, random_vectors, K):
    query_hash = hash_function(query_vector, random_vectors)
    candidate_vectors = lsh_index.get(query_hash, [])
    
    if len(candidate_vectors) == 0:
        return []

    distances = [(euclidean(query_vector, vector), index) for index, vector in candidate_vectors]
    distances.sort()
    return distances[:K]


# Búsqueda por rango usando LSH
def lsh_range_search(query_vector, lsh_index, random_vectors, radius):
    query_hash = hash_function(query_vector, random_vectors)
    candidate_vectors = lsh_index.get(query_hash, [])
    
    results_within_radius = []
    for index, vector in candidate_vectors:
        distance = np.linalg.norm(query_vector - vector)
        if distance <= radius:
            results_within_radius.append((distance, index))
    
    return results_within_radius
