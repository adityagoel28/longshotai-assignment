from pymongo import MongoClient
import urllib

uri = "mongodb+srv://admin:"+ urllib.parse.quote("Admin@123") + "@longshotai.kd4wkfe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.grocery_db
space_collection = db['grocery _collection']
item_type_collection = db['item_type_collection']
item_collection = db['item_collection']