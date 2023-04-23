from tmdbv3api import TMDb
from tmdbv3api import Movie
from connect_mongodb import connect_mongodb
from dotenv import load_dotenv
import os

class Movie_db():  
    def search_value(query):
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        for record in query.values():
            if collection.find_one({'poster_path': record}):
                return False
        return True
    
    def search_movie(query):
        load_dotenv()
        tmdb=TMDb()
        TMDb.api_key = os.getenv("API_KEY")
        tmdb.language = 'en'
        tmdb.debug = True
        movie=Movie()
        return movie.search(query)
    
    def insert_data(query):
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        for record in query.values():
            collection.insert_one({'poster_path': record})

    def remove_data(query):
        db = connect_mongodb.get_db()
        collection = db["movie_db"]

        movie=Movie()
        dictionary = { "poster_path" : stu.poster_path for stu in movie.search(query) }
        for record in dictionary.values():
            collection.delete_one({'poster_path': record}) 
        else:
            similar = query
            collection.delete_one({'poster_path': similar})

    def update_data(query,value):
        load_dotenv()
        TMDb.api_key = os.getenv("API_KEY")

        movie=Movie()
        dictionary = { "poster_path" : stu.poster_path for stu in movie.search(query) }
        update = { "poster_path" : stu.poster_path for stu in movie.search(value) }
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        for record in dictionary.values():
            movie_id = collection.find_one({"poster_path": record})
            collection.update_one({"_id": movie_id["_id"]},{"$set": {"poster_path": update["poster_path"]}})     
        else:
            movie_id = collection.find_one({"poster_path": query})
            collection.update_one({"_id": movie_id["_id"]},{"$set": {"poster_path": update["poster_path"]}})
