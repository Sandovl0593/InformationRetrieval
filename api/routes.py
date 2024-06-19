from api import app
from flask import render_template, jsonify, request
from libs.invertedIndex import InvertedIndex
import psycopg2 as ps
import time
import os

indexfile = InvertedIndex("index_songs.json")

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/query/manual')
def inverted_index():
    # from json request get query and topK
    query = request.json["query"]
    rows = request.json["rows"]

    with open("./dataset/spotify_songs_procesado.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()
        size = len(lines[0].split("@")) - 4

    k = int(request.json["topK"])

    if os.path.exists("index_songs.json"):
        indexfile.load_index()
    else:
        path = f"./dataset/songs_reduced_{rows}.csv" if rows != "all" else f"./dataset/document_songs.csv"
        with open(path, encoding="utf-8", mode="r") as resume_file:
            resume_lines = resume_file.readlines()

        getLyrics = [line.split(" @ ")[2] for line in resume_lines[1:]]
        indexfile.build_index(getLyrics)

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
        "time": round((end - start) * 1000, 4)
    })

@app.post('/api/query/postgres')
def postgres():
    # from json request get query and topK
    query = request.json["query"]
    k = request.json["topK"]
    rows = request.json["rows"]

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
        "time": round((end - start) * 1000, 4)
    })