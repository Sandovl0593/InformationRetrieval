import json
import math
import os
import time
from collections import defaultdict, Counter

class InvertedIndex:
    def __init__(self, index_file):
        self.index_file = index_file
        self.index = defaultdict(list)
        self.idf = {}
        self.length = []
        self.block_files = []

    def text_to_terms(self, text):
        return text.lower().split()

    def spimi_invert(self, token_stream, block_num):
        output_file = f"block_{block_num}.json"
        dictionary = defaultdict(list)
        
        while token_stream:
            doc_id, terms = token_stream.pop(0)
            term_freq = Counter(terms)
            for term, freq in term_freq.items():
                if term not in dictionary:
                    dictionary[term] = []
                dictionary[term].append((doc_id, freq))
        
        sorted_terms = sorted(dictionary.items())
        with open(output_file, 'w') as f:
            json.dump({term: postings for term, postings in sorted_terms}, f)
        
        self.block_files.append(output_file)
        return output_file

    def merge_blocks(self):
        final_index = defaultdict(list)
        
        for block_file in self.block_files:
            with open(block_file, 'r') as f:
                block_index = json.load(f)
                for term, postings in block_index.items():
                    final_index[term].extend(postings)
        
        for term in final_index:
            final_index[term] = sorted(final_index[term])
        
        with open(self.index_file, 'w') as f:
            json.dump(final_index, f)

    def build_index(self, collection_text):
        token_stream = [(doc_id, self.text_to_terms(text)) for doc_id, text in enumerate(collection_text)]
        block_num = 0
        
        while token_stream:
            current_block = token_stream[:1000]  #ajustar
            token_stream = token_stream[1000:]
            self.spimi_invert(current_block, block_num)
            block_num += 1
        
        self.merge_blocks()
        self.calculate_idf_and_length(collection_text)
        
    def calculate_idf_and_length(self, collection_text):
        with open(self.index_file, 'r') as f:
            self.index = json.load(f)
        
        doc_count = len(collection_text)
        term_frequencies = defaultdict(Counter)
        
        for doc_id, text in enumerate(collection_text):
            terms = self.text_to_terms(text)
            term_frequencies[doc_id] = Counter(terms)
        
        tf = defaultdict(lambda: defaultdict(float))
        for term, postings in self.index.items():
            for doc_id, freq in postings:
                tf[term][doc_id] = 1 + math.log10(freq)
            self.idf[term] = math.log10(doc_count / len(postings))
        
        self.length = [0.0] * doc_count
        for term, postings in self.index.items():
            for doc_id, freq in postings:
                tf_idf = tf[term][doc_id] * self.idf[term]
                self.length[doc_id] += tf_idf ** 2
        self.length = [math.sqrt(length) for length in self.length]
        
        self.save_index()

    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump({
                'index': self.index,
                'idf': self.idf,
                'length': self.length
            }, f)

    def load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                data = json.load(f)
                self.index = defaultdict(list, {k: [tuple(post) for post in v] for k, v in data['index'].items()})
                self.idf = data['idf']
                self.length = data['length']
        else:
            raise FileNotFoundError(f"No se encontró el archivo de índice: {self.index_file}")

    def ensure_index(self, collection_text):
        if os.path.exists(self.index_file):
            self.load_index()
        else:
            self.build_index(collection_text)
    
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
            if term in self.index:
                for doc_id, freq in self.index[term]:
                    tf = 1 + math.log10(freq)
                    idf = self.idf[term]
                    doc_tf_idf = tf * idf
                    score[doc_id] += query_vector[term] * doc_tf_idf / (query_length * self.length[doc_id])

        result = sorted(score.items(), key=lambda x: x[1], reverse=True)
        return result[:k]

# Conjunto de datos de prueba
documents = [
    "the cat in the hat",
    "the quick brown fox",
    "jumps over the lazy dog",
    "the fox is quick and the dog is lazy",
    "the dog is not lazy but the fox is quick"
]

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
        results = index.retrieval(query, 3)
        end_time = time.time()
        print(f"Tiempo de respuesta: {end_time - start_time} segundos")
        print("Resultados:")
        for doc_id, score in results:
            print(f"Documento ID: {doc_id}, Score: {score}")

query_interface(index)



