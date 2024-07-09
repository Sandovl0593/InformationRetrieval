from api import app
from flask import jsonify, request
import time
from libs.knn_search import *
import pandas as pd
import os

df = pd.read_csv('../dataset/complete_spotify_with_mfcc.csv')
# Convertir MFCC_Vector de cadena a array de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)

@app.post('/api/audio/knn')
def knn_lineal():
    # from json request get query song
    query = request.json["query"]
    # TODO: Obtener el vector MFCC de UNA canción de consulta
    query_vector = None  

    radius_test = 16.0 # podria ser un request.json["radius"]

    start = time.time()
    results_within_radius = range_search(query_vector, df, radius_test)
    end = time.time()
    tracks = [result['track_name'] for _, result in results_within_radius]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })

