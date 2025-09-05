from movie_storage_sql import add_movie, get_movies, delete_movie, update_movie
"""
# Test adding a movie
add_movie("Inception")
"""
# Test listing movies
movies = get_movies()
for movie in movies:
    print(movie)
"""
# Test updating a movie's rating
update_movie("Inception", 9.0)
print(get_movies())

# Test deleting a movie
delete_movie("Inception")
print(get_movies())  # Should be empty if it was the only movie"""