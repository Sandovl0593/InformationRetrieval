import json
import math
import os
import time
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer


# SE DEBE TENER LA CARPETA TEMP EN EL MISMO DIRECTORIO DEL INDICE Y DESCARGAR LOS PAQUETES PARA LA CONSTRUCCCION DEL INDICE

class InvertedIndex:
    def __init__(self, index_file):
        self.index_file = index_file
        self.idf = {}
        self.length = []
        self.term_to_files = defaultdict(list)
        self.stop_words = set(stopwords.words('english')).union(set(stopwords.words('spanish')))
        self.stemmer_en = PorterStemmer()
        self.stemmer_es = SnowballStemmer('spanish')

    def text_to_terms(self, text):
        words = word_tokenize(text.lower())
        words = [
            self.stemmer_en.stem(word) if word not in stopwords.words('spanish') else self.stemmer_es.stem(word)
            for word in words if word.isalnum() and word not in self.stop_words
        ]
        return words

    def spimi_invert(self, token_stream, block_num):
        dictionary = defaultdict(list)

        while token_stream:
            doc_id, terms = token_stream.pop(0)
            term_freq = Counter(terms)
            for term, freq in term_freq.items():
                dictionary[term].append((doc_id, freq))

        # archivo propio
        for term, postings in dictionary.items():
            if postings:
                output_file = f"temp/{term}_block_{block_num}.json"
                with open(output_file, 'w') as f:
                    json.dump(postings, f)
                self.term_to_files[term].append(output_file)

    def build_index(self, collection_text):
        token_stream = [(doc_id, self.text_to_terms(text)) for doc_id, text in enumerate(collection_text)]
        block_num = 0

        while token_stream:
            current_block = token_stream[:1000]  # depende memoria
            token_stream = token_stream[1000:]
            self.spimi_invert(current_block, block_num)
            block_num += 1

        self.calculate_idf_and_length(collection_text)

    def calculate_idf_and_length(self, collection_text):
        doc_count = len(collection_text)
        tf = defaultdict(lambda: defaultdict(float))

        for term, files in self.term_to_files.items():
            postings = []
            for file in files:
                with open(file, 'r') as f:
                    postings.extend(json.load(f))
            for doc_id, freq in postings:
                tf[term][doc_id] = 1 + math.log10(freq)
            self.idf[term] = math.log10(1 + doc_count / (len(postings) + 1))

        self.length = [0.0] * doc_count
        for term, files in self.term_to_files.items():
            postings = []
            for file in files:
                with open(file, 'r') as f:
                    postings.extend(json.load(f))
            for doc_id, freq in postings:
                tf_idf = tf[term][doc_id] * self.idf[term]
                self.length[doc_id] += tf_idf ** 2
        self.length = [math.sqrt(length) for length in self.length]

        self.save_index()

    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump({
                'idf': self.idf,
                'length': self.length,
                'term_to_files': dict(self.term_to_files)
            }, f)

    def load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                data = json.load(f)
                self.idf = data['idf']
                self.length = data['length']
                self.term_to_files = defaultdict(list, data['term_to_files'])
        else:
            raise FileNotFoundError(f"No se encontró el archivo de índice: {self.index_file}")

    def ensure_index(self, collection_text):
        if os.path.exists(self.index_file):
            self.load_index()
        else:
            self.build_index(collection_text)

    def load_postings(self, term):
        files = self.term_to_files.get(term, [])
        postings = []
        for file in files:
            with open(file, 'r') as f:
                postings.extend(json.load(f))
        return postings

    def retrieval(self, query, k):
        self.load_index()

        query_terms = self.text_to_terms(query)
        query_term_freq = Counter(query_terms)
        query_vector = {}

        for term, freq in query_term_freq.items():
            if term in self.idf:
                tf = 1 + math.log10(freq)
                idf = self.idf[term]
                query_vector[term] = tf * idf

        query_length = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))

        score = defaultdict(float)
        for term in query_vector:
            postings = self.load_postings(term)
            for doc_id, freq in postings:
                tf = 1 + math.log10(freq)
                idf = self.idf[term]
                doc_tf_idf = tf * idf
                score[doc_id] += query_vector[term] * doc_tf_idf / (query_length * self.length[doc_id])

        result = sorted(score.items(), key=lambda x: x[1], reverse=True)
        return result[:k]


'''
# Ejemplo de uso
if __name__ == "__main__":
    import pandas as pd

    # Leer el CSV
    df = pd.read_csv('document_songs.csv', sep='@', names=['text'], header=None)

    # Obtener las primeras 100 líneas del campo 'text'
    documents = df['text'].head(18454).tolist()

    # Crear una instancia del índice invertido
    index = InvertedIndex("test_index.json")

    # Asegurar la construcción del índice
    index.ensure_index(documents)

    # Iniciar la interfaz de consulta
    def query_interface(index):
        while True:
            query = input("Ingrese su consulta (o 'salir' para terminar): ")
            if query.lower() == 'salir':
                break
            start_time = time.time()
            results = index.retrieval(query, 50) #K = 50
            end_time = time.time()
            print(f"Tiempo de respuesta: {end_time - start_time} segundos")
            print("Resultados:")
            for doc_id, score in results:
                print(f"Documento ID: {doc_id}, Score: {score}")

    query_interface(index)'''
