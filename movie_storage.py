import json

def get_movies():
    """reads from json file and returns as python data structure

    Returns:
        list: list of dictionaries with movie title, year and rating
    """
    try:
        with open("movies.json", "r", encoding="utf-8") as fileobj:
            movies = json.loads(fileobj.read())
            return movies
    except FileNotFoundError:
        return None


def save_movies(movies:list):
    """writes movies list of dictionaries to json file

    Args:
        movies (list): list of dictionaries with movie title, year and rating
    """
    movies_json = json.dumps(movies)
    with open("movies.json", "w", encoding="utf-8") as newfile:
        newfile.write(movies_json)


def add_movie(title:str, year:int, rating:float):
    """loads movies, adds new movie and save updated data structure to json file

    Args:
        title (str): movie title
        year (int): release year of the movie
        rating (float): imdb rating
    """
    movies = get_movies()
    if movies is not None:
        movies.append({"title": title, "rating": rating, "year": year})
        save_movies(movies)
        print("Movie added to database")
        print()
        return
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return


def delete_movie(title:str):
    """loads movies, deletes entry with given title and writes movies back to file

    Args:
        title (str): movie title to delete
    """
    movies = get_movies()
    if movies is not None:
        if any(movie.get("title") == title for movie in movies):
            movies = [movie for movie in movies if movie.get("title") != title]
            print("Movie deleted from database")
            save_movies(movies)
            return
        print("Movie is not in the database")
        return
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return


def update_movie(title:str, rating:float):
    """Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it.

    Args:
        title (str): movie title to update
        rating (float): new rating
    """
    movies = get_movies()
    if movies is not None:
        for movie in movies:
            if movie.get("title") == title:
                movie["rating"] = rating
        save_movies(movies)
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return
