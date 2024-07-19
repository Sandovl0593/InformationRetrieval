import os
import time
import numpy as np
import pandas as pd
import librosa
import librosa.display
from PIL import Image
import matplotlib.pyplot as plt
import joblib
import pickle

def hash_function(vector, random_vectors):
    return tuple((vector.dot(random_vector) > 0).astype(int) for random_vector in random_vectors)

def create_lsh_index(data, num_hash_functions, vector_size):
    random_vectors = [np.random.randn(vector_size) for _ in range(num_hash_functions)]
    lsh_index = {}
    for index, row in data.iterrows():
        vector = row[:-1].values.astype(float)
        hash_value = hash_function(vector, random_vectors)
        if hash_value not in lsh_index:
            lsh_index[hash_value] = []
        lsh_index[hash_value].append((index, vector))
    return lsh_index, random_vectors

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

def extract_mel_spectrogram_from_file(file_path, temp_image_path):
    y, sr = librosa.load(file_path, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis="time", y_axis="mel")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Espectrograma de Mel")
    plt.tight_layout()
    plt.savefig(temp_image_path)
    plt.close()

def load_and_flatten_image(image_path):
    img = Image.open(image_path).convert("L")
    img = img.resize((128, 128))
    img_array = np.array(img)
    return img_array.flatten()

csv_file_path = "/Users/smdp/Documents/Probando/500/mel_spectrograms15k.csv"
data = pd.read_csv(csv_file_path)

pca = joblib.load("pca_model15.pkl")
scaler = joblib.load("scaler15.pkl")

query_file_path = "/Users/smdp/Documents/Probando/TracksEnd/TiK ToK.mp3"
temp_image_path = "/Users/smdp/Documents/Probando/temp_mel.png"

extract_mel_spectrogram_from_file(query_file_path, temp_image_path)
query_mel_spectrogram = load_and_flatten_image(temp_image_path)
query_mel_spectrogram_scaled = scaler.transform([query_mel_spectrogram])
query_mel_spectrogram_reducido = pca.transform(query_mel_spectrogram_scaled)

lsh_file_path = "lsh_index15.pkl"
if os.path.exists(lsh_file_path):
    with open(lsh_file_path, "rb") as f:
        lsh_index, random_vectors = pickle.load(f)
else:
    num_hash_functions = 7
    vector_size = len(query_mel_spectrogram_reducido[0])
    lsh_index, random_vectors = create_lsh_index(data, num_hash_functions, vector_size)
    with open(lsh_file_path, "wb") as f:
        pickle.dump((lsh_index, random_vectors), f)

start_time = time.time()
K = 5
neighbors = lsh_knn_search(query_mel_spectrogram_reducido[0], lsh_index, random_vectors, K)
end_time = time.time()

print("Los 8 vecinos más cercanos son:")
for distance, index in neighbors:
    track_info = data.iloc[index]
    print(f"Archivo: {track_info['archivo']}, Distancia: {distance}")
execution_time = end_time - start_time
print(f"El tiempo de ejecución es: {execution_time} segundos")
