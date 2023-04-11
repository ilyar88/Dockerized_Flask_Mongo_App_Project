from pymongo import MongoClient

client = MongoClient(
          host='test_mongodb',
          port=27017,
          username='root',
          password='pass', 
          authSource="admin")    
db = client.users
records = db.register