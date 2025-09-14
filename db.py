from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# connect to mongo atlas cluster

mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Access database 

movie_db = mongo_client["movie_db"]

# pick a collection to operate on
movies_collection = movie_db["saved_movies"]
top_favorite_movies = movie_db["top_three"]