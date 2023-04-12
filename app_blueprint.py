import json
from flask import Flask, Blueprint, jsonify, render_template, request
from tmdbv3api import TMDb
from tmdbv3api import Movie
tmdb=TMDb()
from pymongo import MongoClient

app_blueprint = Blueprint('app_blueprint',__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["movie_db"]
    return db



@app_blueprint.route('/')
def index():
    query = request.args.get('query')
    TMDb.api_key=''
    tmdb.language = 'en'
    tmdb.debug = True
    movie=Movie()
    similar = movie.search(query)
    dictionary = { "poster_path" : stu.poster_path for stu in similar } 
    with open('sample.json', 'w') as file:
     file.write(json.dumps(dictionary))
    return render_template("index.html",image="https://image.tmdb.org/t/p/original/" + str(dictionary["poster_path"]))

@app_blueprint.route('/remove')
def remove():
    query = request.args.get('query')
    db = get_db()
    Collection = db["movie_db"]
    Collection.delete_one(query)

@app_blueprint.route('/movies')
def movies():
    db = get_db()
    with open('sample.json') as file:
        file_data = json.load(file)

    collection = db["movie_db"]

    collection.insert_one(file_data)
    _movie = db.movie_db.find()
    movie = [{"poster_path": m["poster_path"]} for m in _movie]
    return jsonify({"Movies": movie})
    


