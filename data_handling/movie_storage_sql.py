import requests
from sqlalchemy import create_engine, text

# API key and API url
API_key = "c46d7627"
API_URL = "http://www.omdbapi.com"

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT NOT NULL
        )
    """))
    connection.commit()

def get_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()

    return [{"title": row[0], "year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies]

def add_movie(movie_title):
    """Add a new movie to the database."""

    movie_data = prepare_data_for_db(movie_title)
    title = movie_data["title"]
    year = movie_data["year"]
    rating = movie_data["rating"]
    poster_url = movie_data["poster_url"]




    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"),
                               {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            connection.commit()
            print(f"Movie '{movie_title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"), parameters={'title': title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"), {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")


def get_data_from_api(search_term):
    """Get data from API."""
    response = requests.get(url=API_URL, params={"apikey": API_key, "t": search_term})
    if response.ok:
        return response.json()
    else:
        return {}


def prepare_data_for_db(movie_title):
    """Prepare data for DB."""
    #search_term = input("Enter search term: ")
    response = get_data_from_api(movie_title)
    print(response)
    if response["Response"]:
        data_to_return = {}
        data_to_return["title"] = response["Title"]
        data_to_return["year"] = int(response["Year"])
        data_to_return["poster_url"] = response["Poster"]
        ratings = response["Ratings"]
        for rating in ratings:
            if rating["Source"] == "Internet Movie Database":
                data_to_return["rating"] = float(rating["Value"].split("/")[0])
        return data_to_return
    else:
        return {}