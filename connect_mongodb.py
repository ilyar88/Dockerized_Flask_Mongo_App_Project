from pymongo import MongoClient

class connect_mongodb():

    def get_db():
        client = MongoClient(host='test_mongodb',
        port=27017, 
        username='root', 
        password='pass',
        authSource="admin")
        db = client["movie_db"]
        return db