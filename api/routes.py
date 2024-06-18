from api import app
from flask import render_template, jsonify, request
from libs.invertedIndex import InvertedIndex
import psycopg2 as ps

indexfile = InvertedIndex("index_spotify_songs.json")

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/query/manual')
def inverted_index():
    # from json request get query and topK
    query = request.json["query"]

    with open("./dataset/spotify_songs_reduced.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()
        size = len(lines[0].split("@")) - 4

    if not query:
        split_lines = [el.split("@")[:size] for el in lines[1:]]
        return jsonify(split_lines)
    else:
        k = int(request.json["topK"])
        
        # por ahora los lyrics no estan preprocesados
        getLyrics = [line.split("@")[3] for line in lines[1:]]

        indexfile.build_index(getLyrics)
        result = indexfile.retrieval(query, k)

        indexes = []
        for doc_id, _ in result:
            if int(doc_id) not in indexes:
                indexes.append(doc_id)
    
        getLines = [lines[int(index)].split("@")[:size] for index in indexes]
        return jsonify(getLines)

@app.post('/api/query/postgres')
def postgres():
    # from json request get query and topK
    query = request.json["query"]
    k = request.json["topK"]
    print(k, query)

    conn = ps.connect(
        # connection configuration
    )
    cur = conn.cursor()

    # execute query
    if not query:
        cur.execute("SELECT * FROM songs LIMIT %s", (k,))
    else:
        cur.execute("SELECT * FROM songs WHERE lyrics @@ to_tsquery(%s) LIMIT %s", (query, k))
    result = cur.fetchall()

    # close connection
    cur.close()
    conn.close()

    return jsonify(result)