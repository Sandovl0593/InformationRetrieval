from api import app
from flask import render_template, jsonify, request

@app.get('/')
def index():
    return render_template('index.html')


# send data from txt file in format index inverted (dictionary mapping of pair (token, index_line from csv)) to frontend
@app.get('/api/query')
def inverted_index():
    # asumiento que son array de tokens en una query
    tokens = request.args.get('tokens')

    with open("spotify_songs_procesado.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()[1:]

        with open("inverted_index.txt", "r") as file:
            # get csv lines from inverted index file in format "token : index1,index2,..." per line
            lines_index = file.readlines()
            div = [line.split(':') for line in lines_index]
            # create dictionary mapping token to index
            inverted_index = {x[0]: x[1].split(",") for x in div}
        
        # send each row coindicent with index from inverted index filtered by token from params
        indexes, getLines = [], {}
        for token in tokens:
            index_line = inverted_index[token]
            for index in index_line:
                if int(index) not in indexes:
                    indexes.append(index)
    
        getLines = [lines[int(index)] for index in indexes]
    return jsonify(getLines)

@app.get('/api/csv')
def csv():
    with open("./dataset/spotify_songs_reduced.csv", encoding="utf-8", mode="r") as csv_file:
        lines = csv_file.readlines()[1:]
        split_lines = [el.split(",") for el in lines]
   
    return jsonify(split_lines)