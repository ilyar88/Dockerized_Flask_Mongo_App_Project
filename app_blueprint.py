import json
from flask import Flask, Blueprint, render_template, request
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

def search_value(query):
    db = get_db()
    collection = db["movie_db"]
    for record in query.values():
        if collection.find_one({'poster_path': record}):
            return False
    return True

def search_movie(query):
    TMDb.api_key=''
    tmdb.language = 'en'
    tmdb.debug = True
    movie=Movie()
    return movie.search(query)

def insert_data(query):
    db = get_db()
    collection = db["movie_db"]
    for record in query.values():
        collection.insert_one({'poster_path': record})

@app_blueprint.route('/')
def index():
    try:
        similar = search_movie(request.args.get('query'))
        dictionary = { "poster_path" : stu.poster_path for stu in similar }
        if search_value(dictionary):
            insert_data(dictionary)
            temp = dictionary
        else:
            temp = dictionary

        return render_template("index.html",image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
    except:
        return render_template("index.html")


@app_blueprint.route('/remove')
def remove():
    try:
        similar = search_movie(request.args.get('query'))
        dictionary = { "poster_path" : stu.poster_path for stu in similar }
        db = get_db()
        collection = db["movie_db"]
        for record in dictionary.values():
            collection.delete_many({'poster_path': record})

        return render_template("index.html")
    except:
        return render_template("index.html")

@app_blueprint.route('/update')
def update_data():
    try:
        similar = search_movie(request.args.get('query'))
        value = search_movie(request.args.get('value'))

        dictionary = { "poster_path" : stu.poster_path for stu in similar }
        db = get_db()
        collection = db["movie_db"]
        for record in dictionary.values():
            collection.update_one({"poster_path": record},{"$set": {"poster_path": str(value)}})

        return render_template("index.html")
    except:
       return render_template("index.html") 

    
    


