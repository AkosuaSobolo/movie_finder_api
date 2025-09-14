from fastapi import FastAPI, HTTPException, status, Form
from pydantic import BaseModel
from typing import List, Annotated
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


# Configuration of
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = os.getenv("OMDB_URL")

mongo_client = MongoClient(os.getenv("MONGO_URI"))
movie_db = mongo_client["movie_db"]
movies_collection = movie_db["saved_movies"]
top_favorite_movies = movie_db["top_three"]

app = FastAPI()


class FavoriteMovie(BaseModel):
    title: str
    year: str
    genre: str
    imdbID: str
    user_rating: float


# Get a movie by title
@app.get("/movies/{title}")
def get_movie_by_title(title: str):
    query_params = {"t": title, "apikey": OMDB_API_KEY}
    response = requests.get(OMDB_URL, params=query_params)

    if response.status_code!= 200:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Error fetching data from OMDb API"
        )

    movie = response.json()

    if movie.get("Response") == "False":
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Sorry, movie '{title}' not found!"
        )

    return {
        "title": movie.get("Title"),
        "year": movie.get("Year"),
        "genre": movie.get("Genre", "N/A"),
        "imdbID": movie.get("imdbID"),
    }
# Save a movie to favorites
@app.post("/Movies")
def save_to_movies(
    title: Annotated[str, Form(...)],
    genre: Annotated[str, Form(...)],
    year: Annotated[str, Form(...)],
    imdbID: Annotated[str, Form(...)],
    user_rating: Annotated[float, Form(...)],
):
    # Check whether favorite already exists
    if movies_collection.find_one({"imdbID": imdbID}):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Uh-oh! Movie already saved!"
        )

    movies_collection.insert_one(
        {
            "title": title,
            "genre": genre,
            "year": year,
            "imdbID": imdbID,
            "user_rating": user_rating,
        }
    )
    return {"message": "Movie successfully saved!"}


# Get all favorites
@app.get("/All saved movies", response_model=List[FavoriteMovie])
def saved_movies(title: str = "", genre: str = "", limit: int = 5, skip: int = 0):
    query_filter = {
        "$or": [
            {"title": {"$regex": title, "$options": "i"}},
            {"genre": {"$regex": genre, "$options": "i"}},
        ]
    }

    cursor = movies_collection.find(query_filter, {"_id": 0}).skip(skip).limit(limit)
    movies = list(cursor)
    return movies

# Top 3 favorites based on user rating
@app.get("/Favorites")
def top_three():
    top_favorite = list(
        movies_collection.find({}, {"_id": 0}).sort("user_rating", -1).limit(3)
    )
    return top_favorite
