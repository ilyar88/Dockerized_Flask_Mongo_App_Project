from dotenv import load_dotenv
from pymongo import MongoClient
import os

class connect_mongodb():

    def get_db():
        load_dotenv()
        client = MongoClient(host='test_mongodb',
        port=27017, 
        username = os.getenv("USERNAME"), 
        password = os.getenv("PASSWORD"),
        authSource="admin")
        db = client["movie_db"]
        return db
