from api import app
from flask import jsonify, request
import time
from libs.knnSecuencial import *
from libs.knnRtree import *
import pandas as pd
import ast  # Para una conversión segura de strings a listas
import re

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(ast.literal_eval(mfcc_string))

df = pd.read_csv('../dataset/complete_spotify_with_mfcc.csv')
# Convertir MFCC_Vector de cadena a array de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)


@app.post('/api/audio/range/lineal')
def range_lineal():
    # from json request get query song
    query = request.json["query"]
    # TODO: Obtener el vector MFCC de UNA canción de consulta
    query_vector = None  

    radius_test = 16.0 # podria ser un request.json["radius"]

    start = time.time()
    results_within_radius = range_lineal_search(query_vector, df, radius_test)
    end = time.time()
    tracks = [result['track_name'] for _, result in results_within_radius]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })


@app.post('/api/audio/range/rtree')
def range_rtree():
    # from json request get query song
    query = request.json["query"]
    # TODO: Obtener el vector MFCC de UNA canción de consulta
    query_vector = None
    radius_test = 16.0 # podria ser un request.json["radius"]

    start = time.time()
    results_w = range_rtree_search(query_vector, df, radius_test)
    end = time.time()
    tracks = [result['track_name'] for _, result in results_w]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })


@app.post('/api/audio/knn/lineal')
def knn_lineal():
    # from json request get query song
    query = request.json["query"]
    # TODO: Obtener el vector MFCC de UNA canción de consulta
    query_vector = None
    K = 8   # fijo

    start = time.time()
    neighbors = knn_lineal_search(query_vector, df, K)
    end = time.time()
    tracks = [result['track_name'] for _, result in neighbors]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })

@app.post('/api/audio/knn/rtree')
def knn_rtree():
    # from json request get query song
    query = request.json["query"]
    # TODO: Obtener el vector MFCC de UNA canción de consulta
    query_vector = None
    K = 8

    start = time.time()
    neighbors = knn_rtree_search(query_vector, df, K)
    end = time.time()

    tracks = [result['track_name'] for _, result in neighbors]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })
