# movie_finder_api
A simple movie finder api

# FastAPI + MongoDB Movie Favorites App

This project is a simple FastAPI + MongoDB application where you can:

1. Fetch movie details directly from the OMDb API
2. Save movies as favorites in MongoDB
3. List all saved movies with filters and pagination
4. Get the Top 3 favorite movies based on user's rating
5. Built with FastAPI for speed and scalability

## Tech Stack
1. Backend Framework: FastAPI
2. Database: MongoDB
3. External API: OMDb API
4. Environment Management: python-dotenv

## How to Run

1. Clone/download this project  
2. Install dependencies: pip install requirements.txt  
3. Set up .env file in the project root:

OMDB_API_KEY=your_api_key_here
OMDB_URL=http://www.omdbapi.com/
MONGO_URI=mongodb://localhost:27017

4. Start the server: fastapi dev
    
5. Open your browser or Postman at: http://127.0.0.1:8000/docs  

## Endpoints

### Search a movie by title (from OMDb API)

GET /movies/search/{title}

Example request:

GET /movies/search/Inception

Example response:

json
{
  "title": "Inception",
  "year": "2010",
  "genre": "Action, Adventure, Sci-Fi",
  "imdbID": "tt1375666"
}

### Save a movie to favorites

POST /movies

Request (form-data):

json
{
  "title": "Inception",
  "genre": "Action, Adventure, Sci-Fi",
  "year": "2010",
  "imdbID": "tt1375666",
  "user_rating": 9.5
}

Response:

json
{
  "message": "Movie successfully saved!"
}

### Get all saved movies (with filters & pagination)

GET /movies?title=&genre=&limit=5&skip=0

Example request:

GET /movies?genre=Action&limit=2

Example response:

json
[
  {
    "title": "Inception",
    "year": "2010",
    "genre": "Action, Adventure, Sci-Fi",
    "imdbID": "tt1375666",
    "user_rating": 9.5
  },
  {
    "title": "The Dark Knight",
    "year": "2008",
    "genre": "Action, Crime, Drama",
    "imdbID": "tt0468569",
    "user_rating": 9.0
  }
]

### Get Top 3 favorites based on user's rating

GET /movies/favorites

Example response:

json
[
  {
    "title": "Inception",
    "year": "2010",
    "genre": "Action, Adventure, Sci-Fi",
    "imdbID": "tt1375666",
    "user_rating": 9.5
  },
  {
    "title": "The Dark Knight",
    "year": "2008",
    "genre": "Action, Crime, Drama",
    "imdbID": "tt0468569",
    "user_rating": 9.0
 },
  {
    "title": "Interstellar",
    "year": "2014",
    "genre": "Adventure, Drama, Sci-Fi",
    "imdbID": "tt0816692",
    "user_rating": 8.8
  }
]

## Error Handling

a. If OMDb API fails: returns 500 Internal Server Error
b. If movie not found: returns 404 Not Found
c. If movie already exists in favorites: returns 409 Conflict (movie already exists in database)

## Extra Challenge

a. Implemented filtering, skip, and limit (pagination) for all saved movies
b. Added a Top 3 favorites endpoint as well.

## Future Improvements

1. User Authentication & Profiles: Manage personal favorites per user with JWT login
2. User Reviews: Allow comments per movie
3. Caching Layer: Cache OMDb responses to avoid repeated API calls
4. Recommendation Engine: Suggest similar movies based on user favorites
5. Frontend UI: Build a React/Vue interface for easier interaction
6. Testing & CI/CD: Add pytest unit tests and GitHub Actions for automation
7. Deployment: Dockerize and deploy on Render/Railway for live demos
8. Update Movies: Allow users to update their ratings or movie details in favorites
9. Delete Movies: Allow users to remove movies from favorites 
