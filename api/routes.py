from api import app
from flask import render_template, jsonify, request
from libs.invertedIndex import InvertedIndex
import psycopg2 as ps
import time

indexfile = InvertedIndex("index_spotify_songs.json")

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/query/manual')
def inverted_index():
    # from json request get query and topK
    query = request.json["query"]

    with open("./dataset/spotify_songs_procesado.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()
        size = len(lines[0].split("@")) - 4

    if not query:
        split_lines = [el.split("@")[:size] for el in lines[1:]]
        return jsonify({
            "result": split_lines,
            # "time": (end - start) * 1000
        })
    else:
        k = int(request.json["topK"])
        print(query, k)

        with open("./dataset/text_3filas.csv") as resume_file:
            resume_lines = resume_file.readlines()
        
        # por ahora los lyrics no estan preprocesados
        getLyrics = [line.split(" @ ")[2] for line in resume_lines[1:]]

        indexfile.ensure_index(getLyrics)
        start = time.time()
        result = indexfile.retrieval(query, k)
        end = time.time()

        indexes = []
        for doc_id, _ in result:
            if int(doc_id) not in indexes:
                indexes.append(doc_id)
    
        getLines = [lines[int(index)].split("@")[:size] for index in indexes]
        return jsonify({
            "result": getLines,
            "time": (end - start) * 1000
        })

@app.post('/api/query/postgres')
def postgres():
    # from json request get query and topK
    query = request.json["query"]
    k = request.json["topK"]

    conn = ps.connect(
        # connection configuration
    )
    cur = conn.cursor()

    # execute query
    start = time.time()
    if not query:
        cur.execute("SELECT * FROM songs LIMIT %s", (k,))
    else:
        cur.execute("SELECT * FROM songs WHERE lyrics @@ to_tsquery(%s) LIMIT %s", (query, k))
    result = cur.fetchall()
    end = time.time()

    # close connection
    cur.close()
    conn.close()

    return jsonify({
        "result": result,
        "time": (end - start) * 1000
    })