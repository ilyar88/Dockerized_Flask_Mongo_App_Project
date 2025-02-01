from tmdbv3api import TMDb
from tmdbv3api import Movie
from connect_mongodb import connect_mongodb
from dotenv import load_dotenv
import os

class Movie_db():  
    # Function to check if movie poster exists in the database
    def search_value(query):
        # Connect to the MongoDB database
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        
        # Iterate over the query values and check if the poster path is already in the collection
        for record in query.values():
            if collection.find_one({'poster_path': record}):
                return False  # Return False if the record already exists in the database
        return True  # Return True if the record does not exist

    # Function to search for a movie on TMDb using a query string
    def search_movie(query):
        load_dotenv()  # Load environment variables from the .env file
        
        # Set up the TMDb API with the loaded API key
        tmdb = TMDb()
        TMDb.api_key = os.getenv("API_KEY")  # Get the API key from the environment variable
        tmdb.language = 'en'  # Set the language for the TMDb API response
        tmdb.debug = True  # Enable debugging
        movie = Movie()  # Create a Movie object to interact with TMDb
        
        # Return the results of the movie search
        return movie.search(query)

    # Function to insert new movie data into MongoDB
    def insert_data(query):
        # Connect to the MongoDB database
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        
        # Insert each record from the query values into the database collection
        for record in query.values():
            collection.insert_one({'poster_path': record})

    # Function to remove movie data from MongoDB based on a search query
    def remove_data(query):
        # Connect to the MongoDB database
        db = connect_mongodb.get_db()
        collection = db["movie_db"]

        # Create a Movie object to search for movies
        movie = Movie()
        
        # Create a dictionary of poster paths for movies found in the search query
        dictionary = { "poster_path" : stu.poster_path for stu in movie.search(query) }
        
        # Delete each movie from the MongoDB collection based on the poster path
        for record in dictionary.values():
            collection.delete_one({'poster_path': record}) 
        
        else:
            # If no specific movies were found, remove a single similar movie using the query value
            similar = query
            collection.delete_one({'poster_path': similar})

    # Function to update movie data in MongoDB based on a search query and new value
    def update_data(query, value):
        load_dotenv()  # Load environment variables from the .env file
        
        # Set up the TMDb API with the loaded API key
        TMDb.api_key = os.getenv("API_KEY")

        # Create a Movie object to search for movies
        movie = Movie()
        
        # Create dictionaries of poster paths for movies found in the search query and new value
        dictionary = { "poster_path" : stu.poster_path for stu in movie.search(query) }
        update = { "poster_path" : stu.poster_path for stu in movie.search(value) }
        
        # Connect to the MongoDB database
        db = connect_mongodb.get_db()
        collection = db["movie_db"]
        
        # Iterate through the dictionary and update each movie's poster path in the database
        for record in dictionary.values():
            movie_id = collection.find_one({"poster_path": record})
            collection.update_one({"_id": movie_id["_id"]}, {"$set": {"poster_path": update["poster_path"]}})
        
        else:
            # If no matching movie found, update a single movie's poster path using the query value
            movie_id = collection.find_one({"poster_path": query})
            collection.update_one({"_id": movie_id["_id"]}, {"$set": {"poster_path": update["poster_path"]}})
