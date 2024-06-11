import nltk
# Descargar stopwords y punkt de NLTK (Solo se necesita ejecutar la primera vez, luego se comenta)
# nltk.download('stopwords')
# nltk.download('punkt')

import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class TextPreprocessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        self.stop_words = set(stopwords.words('spanish'))
        self.stemmer = SnowballStemmer('spanish')

    def concatenate_fields(self):
        # Concatenar campos textuales en un solo texto por fila
        self.data['text'] = self.data.apply(lambda row: ' '.join([
            str(row['track_name']),
            str(row['track_artist']),
            str(row['lyrics']),
            str(row['track_album_name']),
            str(row['playlist_name']),
            str(row['playlist_genre']),
            str(row['playlist_subgenre']),
            str(row['language'])
        ]), axis=1)

    def tokenize(self, text):
        # Tokenización
        return word_tokenize(text, language='spanish')

    def filter_stopwords(self, tokens):
        # Filtrar stopwords
        return [word for word in tokens if word.lower() not in self.stop_words]

    def stem_words(self, tokens):
        # Aplicar stemming
        return [self.stemmer.stem(word) for word in tokens]

    def preprocess(self):
        self.concatenate_fields()
        self.data['tokens'] = self.data['text'].apply(self.tokenize)
        self.data['filtered_tokens'] = self.data['tokens'].apply(self.filter_stopwords)
        self.data['stemmed_tokens'] = self.data['filtered_tokens'].apply(self.stem_words)
        return self.data

    def save_processed_data(self, output_filepath):
        # Guardar el DataFrame procesado en un nuevo archivo CSV
        self.data.to_csv(output_filepath, index=False)


preprocessor = TextPreprocessor('spotify_songs.csv')
processed_data = preprocessor.preprocess()

# Guardar el DataFrame procesado en un nuevo archivo CSV
preprocessor.save_processed_data('spotify_songs_procesado.csv')

# Mostrando algunas filas del DataFrame procesado
print(processed_data[['text', 'tokens', 'filtered_tokens', 'stemmed_tokens']].head())
