import numpy as np
from heapq import heappush, heappop

# Función para calcular la distancia euclidiana
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Busqueda KNN con cola de prioridad
def knn_lineal_search(query_vector, data, K):
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


def range_lineal_search(query_vector, data, radius, sort_results=True):
    results = []
    for index, row in data.iterrows():
        distance = euclidean_distance(query_vector, row['MFCC_Vector'])
        if distance <= radius:
            results.append((distance, row))
    # Ordenar los resultados por distancia si sort_results es True
    if sort_results:
        results.sort(key=lambda x: x[0])
    return results