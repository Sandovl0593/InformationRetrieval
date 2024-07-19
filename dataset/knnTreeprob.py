import os
import time
import numpy as np
import pandas as pd
import librosa
import librosa.display
from PIL import Image
import matplotlib.pyplot as plt
import joblib
from rtree import index
from typing import Tuple, List

class RtreeKNN:
    def __init__(self, data, index_name, dimension, m=1):
        p = index.Property()
        p.dimension = dimension
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        p.buffering_capacity = m

        data_file = f'{index_name}.data'
        index_file = f'{index_name}.index'
        if os.path.exists(data_file):
            os.remove(data_file)
            print(f"Removed existing data file: {data_file}")
        if os.path.exists(index_file):
            os.remove(index_file)
            print(f"Removed existing index file: {index_file}")

        self.idx = index.Index(index_name, properties=p)

        if data is not None:
            self.data = data
            self._build_index()

    def _build_index(self):
        for i in range(len(self.data)):
            point = tuple(self.data.iloc[i])
            boundingBox = point + point
            self.idx.insert(i, boundingBox)

    def knn_search(self, query_vector, K):
        query_point = tuple(query_vector)
        bounding_box = query_point + query_point
        neighbors = list(self.idx.nearest(bounding_box, K, objects=True))

        def euclidean_distance(point1, point2):
            return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

        result = []
        for neighbor in neighbors:
            point = tuple(self.data.iloc[neighbor.id])
            distance = euclidean_distance(query_point, point)
            result.append((neighbor.id, distance))

        return result

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

csv_file_path = '/Users/smdp/Documents/Probando/500/mel_spectrograms1k.csv'
data = pd.read_csv(csv_file_path)
data_features = data.drop(columns=['archivo'])

pca = joblib.load('pca_model1.pkl')
scaler = joblib.load('scaler1.pkl')

rtree_knn = RtreeKNN(data=data_features, index_name='rtree_index', dimension=pca.n_components_)

while True:
    start_time = time.time()
    query_file_path = '/Users/smdp/Documents/Probando/TracksEnd/TiK ToK.mp3'
    temp_image_path = '/Users/smdp/Documents/Probando/temp_mel.png'

    extract_mel_spectrogram_from_file(query_file_path, temp_image_path)
    query_mel_spectrogram = load_and_flatten_image(temp_image_path)
    query_mel_spectrogram_scaled = scaler.transform([query_mel_spectrogram])
    query_mel_spectrogram_reducido = pca.transform(query_mel_spectrogram_scaled)

    K = 8
    neighbors = rtree_knn.knn_search(query_mel_spectrogram_reducido[0], K)

    print("Los 8 vecinos más cercanos son:")
    for neighbor_id, distance in neighbors:
        print(f"Archivo: {data.iloc[neighbor_id]['archivo']}, Distancia: {distance}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"El tiempo de ejecución es: {execution_time} segundos")
    
    continuar = input("¿Desea realizar otra consulta? (Y/N): ").strip().upper()
    
    if continuar != 'Y':
        break
