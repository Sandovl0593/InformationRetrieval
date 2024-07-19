import os
import time
import numpy as np
import pandas as pd
import librosa
import librosa.display
from PIL import Image
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import joblib

def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

def knn_lineal_search(query_vector, data, K):
    priority_queue = []
    for index, row in data.iterrows():
        vector = row[:-1].values
        distance = euclidean_distance(query_vector, vector)
        heappush(priority_queue, (-distance, (index, row)))
        if len(priority_queue) > K:
            heappop(priority_queue)
    neighbors = []
    while priority_queue:
        neighbors.append(heappop(priority_queue))
    return neighbors[::-1]

def extract_mel_spectrogram_from_file(file_path, temp_image_path):
    y, sr = librosa.load(file_path, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma de Mel')
    plt.tight_layout()
    plt.savefig(temp_image_path)
    plt.close()

def load_and_flatten_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((128, 128))
    img_array = np.array(img)
    return img_array.flatten()

csv_file_path = '/Users/smdp/Documents/Probando/500/mel_spectrograms2k.csv'
data = pd.read_csv(csv_file_path)

pca = joblib.load('pca_model.pkl')
scaler = joblib.load('scaler.pkl')

query_file_path = '/Users/smdp/Documents/Probando/TracksEnd/TiK ToK.mp3'
temp_image_path = '/Users/smdp/Documents/Probando/temp_mel.png'

extract_mel_spectrogram_from_file(query_file_path, temp_image_path)
query_mel_spectrogram = load_and_flatten_image(temp_image_path)
query_mel_spectrogram_scaled = scaler.transform([query_mel_spectrogram])
query_mel_spectrogram_reducido = pca.transform(query_mel_spectrogram_scaled)

expected_shape = data.shape[1] - 1
if query_mel_spectrogram_reducido.shape[1] != expected_shape:
    raise ValueError(f"Error: Dimensión inesperada {query_mel_spectrogram_reducido.shape[1]} para el espectrograma del archivo de consulta. Se esperaba {expected_shape}.")

start_time = time.time()
K = 8
neighbors = knn_lineal_search(query_mel_spectrogram_reducido[0], data, K)
end_time = time.time()
execution_time = end_time - start_time

print("Los 8 vecinos más cercanos son:")
for distance, (index, row) in neighbors:
    print(f"Archivo: {row['archivo']}, Distancia: {-distance}")

print(f"El tiempo de ejecución es: {execution_time} segundos")
