from api import app
from flask import jsonify, request
import time
from libs.knnSecuencial import *
from libs.knnRtree import *
from libs.knnHighD import *
import pandas as pd
from libs.utils import *


df = pd.read_csv('./dataset/mel_spectrogramsEND.csv')

@app.post('/api/audio/knn/lineal')
def knn_lineal():

    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = get_spectrogram_audio(filename, "temp_image.png")
    K = 8

    start = time.time()
    neighbors = knn_lineal_search(query_vector[0], df, K)
    end = time.time()
    tracks = [row['archivo'] for _, (_, row) in neighbors]

    # musics = [get_tracks_from_playlist(id) for id in tracks]
    # result_tracks = [{"name": name, "url": url} for name, url in musics]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })


@app.post('/api/audio/knn/rtree')
def knn_rtree():
    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = get_spectrogram_audio(filename, "temp_image.png")
    K = 8

    start = time.time()
    neighbors = knn_rtree_search(query_vector[0], df, K)
    end = time.time()
    tracks = [row['archivo'] for _, (_, row) in neighbors]

    # musics = [get_tracks_from_playlist(id) for id in tracks]
    # result_tracks = [{"name": name, "url": url} for name, url in musics]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })


@app.post('/api/audio/knn/rtreehighd')
def knn_rtreehighd():
    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = get_spectrogram_audio(filename, "temp_image.png")
    K = 8

    start = time.time()
    num_hash_functions = 2 # Ajustar este valor dependiendo de la dimension del dataset (A mayor dimension mayor num_hash_funcitons)
    vector_size = len(query_vector)
    lsh_index, random_vectors = create_lsh_index(df, num_hash_functions, vector_size)

    neighbors = lsh_knn_search(query_vector[0], lsh_index, random_vectors, K)
    end = time.time()
    tracks = [row['archivo'] for _, (_, row) in neighbors]

    # musics = [get_tracks_from_playlist(id) for id in tracks]
    # result_tracks = [{"name": name, "url": url} for name, url in musics]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })











# @app.post('/api/audio/range/rtree')
# def range_rtree():

#     audio_query = request.files["audio"]
#     filename = request.json["filename"]
#     # download the audio file
#     audio_data = audio_query.read()

#     with open(filename, "wb") as audio_file:
#         audio_file.write(audio_data.content)

#     query_vector = extract_features(filename)

#     radius_test = 16.0 # podria ser un request.json["radius"]

#     start = time.time()
#     results_w = range_rtree_search(query_vector, df, radius_test)
#     end = time.time()
#     tracks = [result['track_name'] for _, result in results_w]

#     return jsonify({
#         "result": tracks,
#         "time": round((end - start) * 1000, 4)
#     })


# @app.post('/api/audio/knn/lineal')
# def knn_lineal():
    
#     audio_query = request.files["audio"]
#     filename = request.json["filename"]
#     # download the audio file
#     audio_data = audio_query.read()

#     with open(filename, "wb") as audio_file:
#         audio_file.write(audio_data.content)

#     query_vector = extract_features(filename)
#     K = 8   # fijo

#     start = time.time()
#     neighbors = knn_lineal_search(query_vector, df, K)
#     end = time.time()
#     tracks = [result['track_name'] for _, result in neighbors]

#     return jsonify({
#         "result": tracks,
#         "time": round((end - start) * 1000, 4)
#     })