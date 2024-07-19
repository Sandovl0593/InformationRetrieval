import numpy as np
import pandas as pd
from heapq import heappush, heappop


# Función para calcular la distancia euclidiana entre dos vectores:
def euclidean_distance(vector1, vector2):
    # Calcula y retorna la norma (distancia euclidiana)
    return np.linalg.norm(vector1 - vector2)

# Función para realizar la búsqueda KNN usando una cola de prioridad:
def knn_lineal_search(query_vector, data, K):
    # Inicializa una lista vacía que actuará como cola de prioridad
    priority_queue = []
    # Itera sobre cada fila del DataFrame
    for index, row in data.iterrows():
        # Toma todos los valores de la fila excepto el último
        vector = row[:-1].values
        # Calcula la distancia euclidiana al vector de consulta
        distance = euclidean_distance(query_vector, vector)
        # Inserta la distancia negativa y la fila en la cola
        heappush(priority_queue, (-distance, (index, row)))
        # Si la cola tiene más de K elementos
        if len(priority_queue) > K:
            # Elimina el elemento con la mayor distancia (mínimo en la cola de distancias negativas)
            heappop(priority_queue)

    # Recolecta y retorna los K vecinos más cercanos
    # Lista para almacenar los vecinos más cercanos
    neighbors = []
    # Mientras hayan elementos en la cola
    while priority_queue:
        # Extrae los elementos de la cola y los añade a la lista de vecinos
        neighbors.append(heappop(priority_queue))
    # Retorna la lista de vecinos en orden de menor a mayor distancia
    return neighbors[::-1]
