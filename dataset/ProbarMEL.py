import os
import numpy as np
import pandas as pd
import librosa
import librosa.display
from PIL import Image
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import joblib

# Función para calcular la distancia euclidiana
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Búsqueda KNN con cola de prioridad
def knn_lineal_search(query_vector, data, K):
    priority_queue = []
    for index, row in data.iterrows():
        vector = row[:-1].values  # Convertir de string a array numpy
        distance = euclidean_distance(query_vector, vector)
        heappush(priority_queue, (-distance, (index, row)))  # Usar distancia negativa para heappop más cercano
        if len(priority_queue) > K:
            heappop(priority_queue)

    # Recolectar y retornar los K vecinos más cercanos
    neighbors = []
    while priority_queue:
        neighbors.append(heappop(priority_queue))
    return neighbors[::-1]






# DESDE ACA SIRVE PARA FRONT 

# Función para extraer el espectrograma de Mel de un archivo de audio y guardarlo como imagen temporal
def extract_mel_spectrogram_from_file(file_path, temp_image_path):
    y, sr = librosa.load(file_path, sr=None)

    # Calcular el espectrograma de Mel
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

    # Convertir el espectrograma a escala de decibelios
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Guardar el espectrograma de Mel como una imagen temporal
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma de Mel')
    plt.tight_layout()
    plt.savefig(temp_image_path)
    plt.close()

# Función para cargar la imagen del espectrograma y convertirla a vector aplanado
def load_and_flatten_image(image_path):
    img = Image.open(image_path).convert('L')  # Convertir a escala de grises
    img = img.resize((128, 128))  # Redimensionar la imagen a 128x128
    img_array = np.array(img)  # Convertir la imagen a array (manteniendo la estructura bidimensional)
    return img_array.flatten()  # Aplanar la imagen

# Leer el archivo CSV con los espectrogramas de Mel
csv_file_path = '/Users/smdp/Documents/Probando/500/mel_spectrogramsEND.csv'
data = pd.read_csv(csv_file_path)

# Cargar el modelo PCA y el scaler guardados
pca = joblib.load('pca_model.pkl')
scaler = joblib.load('scaler.pkl')

# Seleccionar un track específico desde un path y convertirlo a su vector de características de espectrograma de Mel
query_file_path = '/Users/smdp/Documents/Probando/TracksEnd/Arrogant.mp3'  # Reemplaza con la ruta del archivo de audio que deseas probar
temp_image_path = '/Users/smdp/Documents/Probando/temp_mel.png'

# Extraer el espectrograma de Mel y guardarlo como imagen temporal
extract_mel_spectrogram_from_file(query_file_path, temp_image_path)

# Cargar la imagen y convertirla a vector aplanado
query_mel_spectrogram = load_and_flatten_image(temp_image_path)

# Escalar el espectrograma de consulta utilizando el mismo scaler usado para los datos originales
query_mel_spectrogram_scaled = scaler.transform([query_mel_spectrogram])

# Aplicar PCA para reducir dimensionalidad del espectrograma de consulta
query_mel_spectrogram_reducido = pca.transform(query_mel_spectrogram_scaled)

# Verificar que las dimensiones sean consistentes
expected_shape = data.shape[1] - 1  # Excluyendo la columna 'archivo'
if query_mel_spectrogram_reducido.shape[1] != expected_shape:
    raise ValueError(f"Error: Dimensión inesperada {query_mel_spectrogram_reducido.shape[1]} para el espectrograma del archivo de consulta. Se esperaba {expected_shape}.")

# Depuración: imprimir las dimensiones y los primeros elementos
print(f"Dimensión del espectrograma de consulta: {query_mel_spectrogram_reducido.shape[1]}")
print(f"Primeros 5 elementos del espectrograma de consulta: {query_mel_spectrogram_reducido[0, :5]}")
print(f"Dimensión de los vectores del CSV: {expected_shape}")
print(f"Primeros 5 elementos del primer vector del CSV: {data.iloc[0, :-1].values[:5]}")

# Usar la función KNN para encontrar los 3 vecinos más cercanos
K = 5
neighbors = knn_lineal_search(query_mel_spectrogram_reducido[0], data, K)

# Imprimir los resultados
print("Los 3 vecinos más cercanos son:")
for distance, (index, row) in neighbors:
    print(f"Archivo: {row['archivo']}, Distancia: {-distance}")
