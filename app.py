import json
from flask import Flask, jsonify, request
from tmdbv3api import TMDb
from tmdbv3api import Movie
tmdb=TMDb()
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["people_db"]
    return db

@app.route('/search')
def search():
    query = request.args.get('query')
    json_list = []
    TMDb.api_key=''
    tmdb.language = 'en'
    tmdb.debug = True
    movie=Movie()
    similar = movie.search(query)
    with open('sample.json', 'w' ,encoding='utf-8') as f:
        for line in similar:
            f.write(f"{line}\n")
    return "Welcome!"

@app.route('/people_db')
def get_stored_people_db():
    db = get_db()
    with open('sample.json' ,encoding='utf-8') as file:
        file_data = json.load(file)
     
    Collection = db["people_db"]

    Collection.insert_many(file_data)
    
if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
