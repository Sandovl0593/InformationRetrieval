import numpy as np
import librosa
import librosa.display
from PIL import Image
import matplotlib.pyplot as plt
import joblib
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


# Función para cargar la imagen del espectrograma y convertirla a vector aplanado
def load_and_flatten_image(image_path):
    img = Image.open(image_path).convert('L')  
    img = img.resize((128, 128))  
    img_array = np.array(img)  
    return img_array.flatten() 


def get_spectrogram_audio(query_file_path, temp_image_path):
    # Cargar el modelo PCA y el scaler guardados
    pca = joblib.load('pca_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Extraer el espectrograma de Mel y guardarlo como imagen temporal
    extract_mel_spectrogram_from_file(query_file_path, temp_image_path)

    # Cargar la imagen y convertirla a vector aplanado
    query_mel_spectrogram = load_and_flatten_image(temp_image_path)

    # Escalar el espectrograma de consulta utilizando el mismo scaler usado para los datos originales
    query_mel_spectrogram_scaled = scaler.transform([query_mel_spectrogram])

    # Aplicar PCA para reducir dimensionalidad del espectrograma de consulta
    query_mel_spectrogram_reducido = pca.transform(query_mel_spectrogram_scaled)

    return query_mel_spectrogram_reducido