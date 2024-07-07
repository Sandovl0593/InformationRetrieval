#script que hace crecer el dataset segun el id de las playlist en Spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd
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
            track_info = {
                "track_id": track['id'],
                "track_name": track['name'],
                "track_artist": ", ".join([artist['name'] for artist in track['artists']]),
                "track_preview": track['preview_url']
            }
            track_list.append(track_info)

    return track_list


def search_tracks_by_name(track_name, limit=50):
    results = spotify.search(q=track_name, type='track', limit=limit)
    tracks = results['tracks']['items']
    track_list = []

    for track in tracks:
        if track['preview_url']:  # Solo añadir si tiene preview_url
            track_info = {
                "track_id": track['id'],
                "track_name": track['name'],
                "track_artist": ", ".join([artist['name'] for artist in track['artists']]),
                "track_preview": track['preview_url']
            }
            track_list.append(track_info)

    return track_list


def save_tracks_to_csv(track_list, filename):
    # Leer el CSV existente si existe
    try:
        existing_df = pd.read_csv(filename)
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    new_df = pd.DataFrame(track_list)

    # Concatenar los datos nuevos con los existentes
    combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='track_id').reset_index(drop=True)

    # Guardar de nuevo en el CSV
    combined_df.to_csv(filename, index=False)


if __name__ == "__main__":
    # Para poder obtener canciones de una playlist:
    playlist_id = '37i9dQZF1DZ06evO3paMmc'  # id de la playlist
    tracks_from_playlist = get_tracks_from_playlist(playlist_id)
    save_tracks_to_csv(tracks_from_playlist, 'playlist_tracks.csv')

    # Para buscar canciones por nombre
    # track_name = 'Shape of You'  # nombre de la canción
    # searched_tracks = search_tracks_by_name(track_name)
    # save_tracks_to_csv(searched_tracks, 'searched_tracks.csv')
