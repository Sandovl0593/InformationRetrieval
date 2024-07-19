#este script descarga los audios y los pone en la carpeta "downloaded_audio" y genera un csv que es el mismo que el de "playlist_tracks" solo que añade tmbn al csv resultante la columna "mfcc"
# <- (script 0)
import os
import requests
import librosa
import re
import pandas as pd
import numpy as np


def extract_audio_features(playlist_df):
    audio_features = [f"MFCC{index + 1}" for index in range(20)]
    audio_features.append('mp3_file')
    features_df = pd.DataFrame(columns=audio_features)

    # Directorio para los archivos de audio:
    audio_dir = 'downloaded_audio'
    os.makedirs(audio_dir, exist_ok=True)

    for index in range(len(playlist_df)):
        track_name = re.sub(r'\W+', '', playlist_df.iloc[index].track_name)
        artist_name = re.sub(r'\W+', '', playlist_df.iloc[index].track_artist)
        preview_url = playlist_df.iloc[index].track_preview
        file_name = f"_{track_name}_{artist_name}.mp3"

        # Truncar el nombre del archivo si es demasiado largo
        if len(file_name) > 100:  # Truncar a partir de 100 caracteres
            file_name = file_name[:100] + ".mp3"

        file_path = os.path.join(audio_dir, file_name)

        # Verificar si el directorio existe
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        audio_data = requests.get(preview_url)

        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data.content)

        features_df.loc[index, 'mp3_file'] = file_path

        audio_series, sample_rate = librosa.load(file_path)

        mfcc_matrix = librosa.feature.mfcc(y=audio_series, sr=sample_rate)
        mfcc_mean = np.mean(mfcc_matrix, axis=1).reshape(1, -1)
        for coef in range(20):
            features_df.loc[index, f"MFCC{coef + 1}"] = mfcc_mean[0][coef]
    return features_df


# Cargando el dataset
playlist_df = pd.read_csv('playlist_tracks.csv')
# select random rows to fill 1000 rows
playlist_dfff = playlist_df.sample(n=1000, random_state=42)
# download the reduced dataset
playlist_dfff.to_csv('reduced_playlist_tracks.csv', index=False)
# por temas de tiempo

features_df = extract_audio_features(playlist_dfff)

mfcc_columns = [f"MFCC{i}" for i in range(1, 21)]
features_df['MFCC_Vector'] = features_df[mfcc_columns].apply(lambda row: row.tolist(), axis=1)
features_df.drop(mfcc_columns, axis=1, inplace=True)

features_df['MFCC_Vector'] = features_df['MFCC_Vector'].apply(np.array)

combined_df = pd.concat([playlist_df.reset_index(), features_df.reset_index()], axis=1)
combined_df.drop(columns=['index'], inplace=True)

combined_df.to_csv('complete_spotify_with_mfcc.csv', index=False)
print(combined_df.info())

