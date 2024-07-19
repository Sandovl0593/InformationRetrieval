from api import app
from flask import jsonify, request
import time
from libs.knnSecuencial import *
from libs.knnRtree import *
import pandas as pd
import ast  # Para una conversión segura de strings a listas
import re
import librosa
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import warnings

warnings.filterwarnings('ignore')

# Credenciales de Spotipy
SPOTIPY_CLIENT_ID = '42af1dc139184fc09475bdf54c5029cf'
SPOTIPY_CLIENT_SECRET = '88f14ed5fb394c08813dddcd9656d821'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = "user-library-read playlist-read-private"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))


def get_tracks_from_playlist(playlist_id):
    results = spotify.playlist(playlist_id)
    tracks = results['tracks']['items']
    track_list = []

    while results['tracks']['next']:
        results = spotify.next(results['tracks'])
        tracks.extend(results['tracks']['items'])

    for item in tracks:
        track = item['track']
        if track['preview_url']:  # Solo añadir si tiene preview_url
            track_list.append((track['name'], track['preview_url']))

    return track_list

# Función para convertir una cadena de MFCC_Vector en un vector numpy
def parse_mfcc_vector(mfcc_string):
    # Reemplazar caracteres innecesarios y añadir comas
    mfcc_string = re.sub(r'(\d)\s+([-]?\d)', r'\1,\2', mfcc_string.replace('\n', ' '))
    return np.array(ast.literal_eval(mfcc_string))

def extract_features(audio_file):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfccs_mean = np.mean(mfccs, axis=1)
    return mfccs_mean

df = pd.read_csv('./dataset/complete_spotify_with_mfcc.csv')
# Convertir MFCC_Vector de cadena a array de numpy
df['MFCC_Vector'] = df['MFCC_Vector'].apply(parse_mfcc_vector)


@app.post('/api/audio/range/lineal')
def range_lineal():

    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = extract_features(filename)
    radius_test = 16.0

    start = time.time()
    results_within_radius = range_lineal_search(query_vector, df, radius_test)
    end = time.time()
    tracks = [result['track_id'] for _, result in results_within_radius]

    musics = [get_tracks_from_playlist(id) for id in tracks]
    result_tracks = [{"name": name, "url": url} for name, url in musics]
    
    return jsonify({
        "result": result_tracks,
        "time": round((end - start) * 1000, 4)
    })


@app.post('/api/audio/range/rtree')
def range_rtree():

    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = extract_features(filename)

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
    
    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = extract_features(filename)
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
    audio_query = request.files["audio"]
    filename = request.json["filename"]
    # download the audio file
    audio_data = audio_query.read()

    with open(filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    query_vector = extract_features(filename)
    K = 8

    start = time.time()
    neighbors = knn_rtree_search(query_vector, df, K)
    end = time.time()

    tracks = [result['track_name'] for _, result in neighbors]

    return jsonify({
        "result": tracks,
        "time": round((end - start) * 1000, 4)
    })
