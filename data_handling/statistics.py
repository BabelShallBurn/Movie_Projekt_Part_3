import matplotlib.pyplot as plt
import numpy as np
import data_handling.movie_storage_sql as ms

def stats():
    """
    calculates and prints following stats:
      - average rating
      - median rating
      - highest rating and the corresponding movie
      - lowest rating and the corresponding movie

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    movies = ms.get_movies()
    if movies is not None:
        ratings_sorted = sorted(movie.get("rating") for movie in movies)
        average_rating = round(sum(ratings_sorted) / len(movies), 1)
        median_rating = 0
        highest_rating = max(ratings_sorted)
        highest_rated_movies = ""
        lowest_rating = min(ratings_sorted)
        lowest_rated_movies = ""

        if len(movies) % 2 == 0:
            median_rating = (ratings_sorted[len(movies) // 2 - 1] + ratings_sorted[len(movies) // 2]) / 2
        elif len(movies) % 2 != 0:
            median_rating = ratings_sorted[len(movies) // 2]

        for movie in movies:
            if movie.get("rating") == lowest_rating:
                lowest_rated_movies += f"{movie.get("title")}, "
            if movie.get("rating") == highest_rating:
                highest_rated_movies += f"{movie.get("title")}, "

        print(f"The average rating is {average_rating}.")
        print(f"The median rating is {median_rating}")
        print(f"The lowest rated movie(s) is (are): {lowest_rated_movies}with a score of {lowest_rating}")
        print(f"The highest rated movie(s) is (are): {highest_rated_movies}with a score of {highest_rating}")
        return
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return


def sort_movies():
    """
    prints out a rating sorted list of the movies in the database

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    while True:
        print("1. Sort by rating")
        print("2. Sort by year")
        print()
        user_input = input("Enter choice (1 or 2): ")
        print()
        try:
            if not user_input.isnumeric():
                raise ValueError("Please enter 1 or 2.")
            if user_input.isnumeric():
                if user_input != "1" and user_input != "2":
                    raise ValueError("Please enter 1 or 2.")

            if user_input == "1":
                movies = ms.get_movies()
                if movies is not None:
                    sorted_ratings = sorted(movies, key=lambda movie: movie.get("rating", 0), reverse=True)
                    for movie in sorted_ratings:
                        print(f"{movie.get("title")}: {movie.get("rating")} from {movie.get("year")}")
                    return
                else:
                    print("Couldn't find movies.json file. Please check directory for file.")
                    return
            elif user_input == "2":
                movies = ms.get_movies()
                if movies is not None:
                    sorted_years = sorted(movies, key=lambda movie: movie.get("year", 0))
                    for movie in sorted_years:
                        print(f"{movie.get("title")}: {movie.get("rating")} from {movie.get("year")}")
                    return
                else:
                    print("Couldn't find movies.json file. Please check directory for file.")
                    return
        except ValueError as e:
            print("Error:", e)


def filter_movies():
    """filters movies for rating and / or year

    Raises:
        ValueError: checks if rating is float
        ValueError: checks if year is int
        ValueError: checks if year is int
    """
    end_year = 2500
    start_year = 1900
    minimum_rating = 0.0
    while True:
        minimum_rating_str = input("Enter minimum rating (leave blank for no minimum rating): ")
        start_year_str = input("Enter start year (leave blank for no start year): ")
        end_year_str = input("Enter end year (leave blank for no end year): ")
        print()

        try:
            if crud.is_not_float(minimum_rating_str) and minimum_rating_str != "":
                raise ValueError("Rating must be a decimal number!")
            if not crud.is_not_float(minimum_rating_str):
                if not 0 <= float(minimum_rating_str) <= 10:
                    raise ValueError("Rating must be between 0 and 10!")

            if not start_year_str.isnumeric() and start_year_str != "":
                raise ValueError("Start and end year must be a four digit integer or left empty!")
            if start_year_str.isnumeric():
                if not 1900 <= int(start_year_str) <= 2026:
                    raise ValueError("Start year must be between 1900 and 2026!")

            if not end_year_str.isnumeric() and end_year_str != "":
                raise ValueError("Start and end year must be a four digit integer or left empty!")
            if end_year_str.isnumeric():
                if not "1900" <= end_year_str <= "2026" and end_year_str != "":
                    raise ValueError("End year must be between 1900 and 2026!")
            if start_year_str.isnumeric() and end_year_str.isnumeric():
                if int(start_year_str) > int(end_year_str):
                    raise ValueError("Start year has to be smaller than end year!")

            if end_year_str != "":
                end_year = int(end_year_str)
            if start_year_str != "":
                start_year = int(start_year_str)
            if minimum_rating_str != "":
                minimum_rating = float(minimum_rating_str)

            movies = ms.get_movies()
            if movies is not None:
                print("Filtered Movies:")
                print()

                for movie in movies:
                    if start_year < movie.get("year") < end_year and movie.get("rating") > minimum_rating:
                        title = movie.get("title")
                        rating = movie.get("rating")
                        year = movie.get("year")
                        print(f"{title} ({year}): {rating}")
                return
            else:
                print("Couldn't find movies.json file. Please check directory for file.")
                return
        except ValueError as e:
            print("Error:", e)


def create_rating_histogram():
    """
    creates a histogram of the movie ratings using the matplotlib library

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    movies = ms.get_movies()
    if movies is not None:
        file_name = input("Please set a file name: ")
        data = np.array(list(movie.get("rating") for movie in movies))
        plt.hist(data, bins=5)
        plt.xlabel('ratings')
        plt.ylabel('occurences')
        plt.savefig(file_name)
        print("File created")
        return
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return