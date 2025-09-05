import random
import matplotlib.pyplot as plt
import numpy as np
from fuzzysearch import find_near_matches
import movie_storage_sql as ms


def main():
    """
    main function where the print_menu function is called
    """
    # Your code here
    print_menu()


def print_menu():
    """
    prints menu to the terminal and asks user for input.
    based on user input the corresponding function is called

    Args:
        movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    while True:
        print()
        print("********** My Movies Database **********")
        print()
        print(
            "Menu \n 0. Exit \n 1. List Movies \n 2. Add movie \n 3. Delete movie \n 4. Update movie \n 5. Stats \n 6. Random movie \n 7. Search movie \n 8. Sort movies by rating or year \n 9. Save a histogram of the ratings to png-file \n 10. Filter Movies for year and rating\n 11. Create html")
        print()
        user_input = input("Enter choice (0-11): ")
        try:
            if not user_input.isnumeric():
                raise ValueError("Please enter a number between 0 and 11.")
            if user_input.isnumeric():
                if not 0 <= int(user_input) <= 11:
                    raise ValueError("Please enter a number between 0 and 11.")
            if user_input == "0":
                print("Bye")
                break
            elif user_input == "1":
                list_movies()
            elif user_input == "2":
                add_movie()
            elif user_input == "3":
                delete_movie()
            elif user_input == "4":
                update_movie()
            elif user_input == "5":
                stats()
            elif user_input == "6":
                random_movie()
            elif user_input == "7":
                search_movie()
            elif user_input == "8":
                sort_movies()
            elif user_input == "9":
                create_rating_histogram()
            elif user_input == "10":
                filter_movies()
            elif user_input == "11":
                create_html()
        except ValueError as e:
            print("Error:", e)
        print()


def list_movies():
    """
    prints size of database and lists every movie and its corresponding rating
    """
    movies = ms.get_movies()
    if movies is not None:
        print(f"{len(movies)} in total")
        print()
        for movie in movies:
            print(f"{movie["title"]} from {movie["year"]}: {movie["rating"]}")
        print()
        return
    else:
        print("Couldn't find movies.json file. Please check directory for file.")
        return


def add_movie():
    """
    allows user to add a movie and its rating if it is not in the database
    """
    while True:
        movie_to_add = input("Name a movie to add: ")
        #rating_to_add = input("What's the rating for this movie? ")
        #year_to_add = input("Enter the year: ")
        try:
            if movie_to_add == "":
                raise ValueError("Movie must not be empty!")


            ms.add_movie(movie_to_add)
            return
        except ValueError as e:
            print("Error:", e)
            print()


def delete_movie():
    """
    allows user to delete movie and its rating

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
    while True:
        movie_to_delete = input("Name a movie to delete: ")
        try:
            if movie_to_delete == "":
                raise ValueError("Movie must not be empty!")
            ms.delete_movie(movie_to_delete)
            return
        except ValueError as e:
            print("Error:", e)


def update_movie():
    """
    updates rating of a movie in the database

    Args:
      movies (dict): list of dictionaries where movies, years of release and ratings are stored
    """
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
            print("Error:", e)


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
        print("Couldn't find movies.json file. Please check directory for file.")
        return


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
            if is_not_float(minimum_rating_str) and minimum_rating_str != "":
                raise ValueError("Rating must be a decimal number!")
            if not is_not_float(minimum_rating_str):
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


def load_html(file_path):
    """ Loads a HTML file """
    with open(file_path, "r", encoding="utf-8") as fileobj:
        html_content = fileobj.read()
        return html_content


def create_html():
    data = ms.get_movies()
    html_data = load_html('index_template.html')
    movie_html_list = ""
    for movie in data:
        movie_html_list += '<li>\n'
        movie_html_list += '    <div class="movie">\n'
        movie_html_list += f'        <img class="movie-poster" src="{movie['poster_url']}">\n'
        movie_html_list += f'        <div class="movie-title">{movie["title"]}</div>\n'
        movie_html_list += f'        <div class="movie-year">{movie["year"]}</div>\n'
        movie_html_list += "    </div>\n"
        movie_html_list += '</li>\n'

    html_data = html_data.replace("__TEMPLATE_MOVIE_GRID__", movie_html_list)
    html_data = html_data.replace("__TEMPLATE_TITLE__","Eric's Movies")

    with open("index.html", "w", encoding="utf-8") as fileobj:
        fileobj.write(html_data)

    print("Created index.html file")
    return


def is_not_float(num):
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


if __name__ == "__main__":
    main()
