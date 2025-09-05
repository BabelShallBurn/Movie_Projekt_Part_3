import data_handling.movie_storage_sql as ms

def create_website():
    """ Creates a HTML file from database data. """
    data = ms.get_movies()
    html_data = load_html('templates/index_template.html')
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
    html_data = html_data.replace("style.css", "templates/style.css")

    with open("index.html", "w", encoding="utf-8") as fileobj:
        fileobj.write(html_data)

    print("Created index.html file")
    return

def load_html(file_path):
    """ Loads a HTML file from given path. """
    with open(file_path, "r", encoding="utf-8") as fileobj:
        html_content = fileobj.read()
        return html_content