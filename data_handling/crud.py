import random
from fuzzysearch import find_near_matches
import data_handling.movie_storage_sql as ms


def list_movies():
    """
    prints size of database and lists every movie and its corresponding rating
    """
    movies = ms.get_movies()
    if movies != []:
        print(f"{len(movies)} in total")
        print()
        for movie in movies:
            print(f"{movie["title"]} from {movie["year"]}: {movie["rating"]}")
        print()
        return
    else:
        print("No movie data available")
        return


def add_movie():
    """
    allows user to add a movie and its rating if it is not in the database
    """
    while True:
        movie_to_add = input("Name a movie to add: ")
        movies = ms.get_movies()
        movie_exists = False
        try:
            if movie_to_add == "":
                raise ValueError("Movie must not be empty!")
            for movie in movies:
                if movie["title"] == movie_to_add:
                    movie_exists = True
            if movie_exists:
                raise ValueError("Movie already exists!")
            ms.add_movie(movie_to_add)
            return
        except ValueError as e:
            print("Couldn't add movie to database! Error:", e)
            print()


def delete_movie():
    """ Allows user to delete movie and its rating. """
    while True:
        movie_to_delete = input("Name a movie to delete: ")
        movies = ms.get_movies()
        movie_exists = False
        try:
            if movie_to_delete == "":
                raise ValueError("Movie must not be empty!")
            for movie in movies:
                if movie["title"] == movie_to_delete:
                    movie_exists = True
            if not movie_exists:
                raise ValueError("Movie not found!")

            ms.delete_movie(movie_to_delete)
            return
        except ValueError as e:
            print("Couldn't delete movie! Error:", e)
            print()


def update_movie():
    """ Updates rating of a movie in the database. """
    while True:
        movie_to_update = input("Name a movie to update: ")
        rating_to_update = input("What's the new rating for this movie? ")

        try:
            if movie_to_update == "":
                raise ValueError("Movie must not be empty!")
            if is_not_float(rating_to_update) or not 0 <= float(rating_to_update) <= 10:
                raise ValueError("Rating must be a decimal number between 0 and 10!")
            rating_to_update_float = float(rating_to_update)
            ms.update_movie(movie_to_update, rating_to_update_float)
            return
        except ValueError as e:
            print("Couldn't update database! Error:", e)
            print()


def is_not_float(num:str):
    """helping function to check if a string is not a float

    Args:
        num (str): input string

    Returns:
        bool: true if float
    """
    try:
        float(num)
        return False
    except ValueError:
        return True


def search_movie():
    """
    allows user to search for a movie using the fuzzysearch library
    so spelling must not be a 100 % perfect

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    movies = ms.get_movies()
    if movies is not None:
        string_to_search = input("Enter part of a movie name: ")
        while True:
            try:
                if string_to_search == "":
                    raise ValueError("Movie must not be empty!")
                for movie in movies:
                    if movie.get("title").lower() == string_to_search.lower():
                        print(f"{movie.get("title")} from {movie.get("year")} with a rating of {movie.get("rating")}")
                        return

                list_of_possible_movies = []
                for movie in movies:
                    if find_near_matches(string_to_search.lower(), movie.get("title").lower(), max_substitutions=1,
                                         max_insertions=1, max_deletions=1, max_l_dist=2) != []:
                        list_of_possible_movies.append(movie.get("title"))
                if list_of_possible_movies:
                    print(f"The movie '{string_to_search}' does not exist. Did you mean: ")
                    print()
                    for possible_movie in list_of_possible_movies:
                        print(possible_movie)
                else:
                    print("No matches found.")
                return
            except ValueError as e:
                print("Error:", e)
                return
    else:
        print("Couldn't find any movies!")
        return


def random_movie():
    """
    prints out a random chosen movie with its rating

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    movies = ms.get_movies()
    if movies is not None:
        rand_movie = random.choice(movies)
        print(f"Random movie: {rand_movie["title"]} from {rand_movie["year"]} with a rating of {rand_movie["rating"]}")
        return
    else:
        print("Couldn't find any movies.")
        return
