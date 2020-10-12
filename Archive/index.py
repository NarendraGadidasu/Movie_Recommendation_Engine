import numpy as np
import json
import csv
import collections
from flask import Flask, render_template
from flask import request
import Movie_Class
import sim_new

app = Flask(__name__, static_folder='static')

database = sim_new.MovieData('all_movies_2000.csv', 'movie_list_updated.csv')


@app.route('/GetMoviesTMDB', methods=["GET"])
def GetMoviesTMDB():
    data_path = 'movie_tmdb_updated.csv'
    with open(data_path, encoding='utf-8') as j:
        data = j.readlines()
        keys = data[0].rstrip().split(',')
        values = data[1:]
        dictVal = [dict(zip(keys, d.rstrip().split(','))) for d in values]

    return json.dumps(dictVal)


@app.route('/GetMovies', methods=["GET"])
def GetMovies():
    data_path = 'movie_list_updated.csv'
    with open(data_path, encoding='utf-8') as j:
        data = j.readlines()
        keys = data[0].rstrip().split(',')
        values = data[1:]
        dictVal = [dict(zip(keys, d.rstrip().split(','))) for d in values]

    return json.dumps(dictVal)


@app.route('/GetSimilarMovies', methods=["GET"])
def GetSimilarMovies():
    req = request.args.get('MovieList')
    #req = "215, 158, 373, 512, 267"
    user_movies_idx = [int(i) for i in req.split(',')]
    print(user_movies_idx)
    req = request.args.get('weights')
    trope_weights = None
    if req is not None:
        trope_weights = [float(i) for i in req.split(',')]
    print(trope_weights)

    return database.getSimilarMovies(user_movies_idx, trope_weights)


@app.route('/ui', methods=["GET"])
def root():
    return render_template('index.html')


if __name__ == '__main__':
    # GetSimilarMovies()
    app.run(debug=True)
