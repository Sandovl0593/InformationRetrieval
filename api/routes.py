from api import app
from flask import render_template, jsonify, request
from libs.invertedIndex import InvertedIndex

indexfile = InvertedIndex("index_spotify_songs.json")

@app.get('/')
def index():
    return render_template('index.html')


# send data from txt file in format index inverted (dictionary mapping of pair (token, index_line from csv)) to frontend
@app.get('/api/query')
def inverted_index():
    # asumiento que son array de tokens en una query
    query = request.args.get('query')
    k = request.args.get('topK')

    with open("spotify_songs_procesado.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()
        size = len(lines[0].split("@")) - 4

        # create index from csv only list of celds of position 3 (lyrics)
        # indexfile.ensure_index([line.split("@")[3] for line in lines[1:]])
        result = indexfile.retrieval(query, k)
        
        # send each row coindicent with index from inverted index filtered by token from params
        indexes = []
        for doc_id, _ in result:
            if int(doc_id) not in indexes:
                indexes.append(doc_id)
    
        getLines = [lines[int(index)].split("@")[:size] for index in indexes]
    return jsonify(getLines)

@app.get('/api/csv')
def csv():
    with open("./dataset/spotify_songs_reduced.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()
        size = len(lines[0].split("@")) - 4

        split_lines = [el.split("@")[:size] for el in lines[1:]]
   
    return jsonify(split_lines)