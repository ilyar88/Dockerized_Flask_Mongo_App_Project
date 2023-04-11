
from tmdbv3api import TMDb, Movie

# Initialize TMDb and Movie objects
tmdb = TMDb()
movie = Movie()

# Set your unique API key that you get from TMDB after registration. In this case, the API key is set as a class variable.
tmdb.api_key = '570f084693ffde2a779a4ed58043737d'

# Search for movies with the query 'Mad Max'
search_result = movie.search('avatar')

# Loop through each movie in the search results and print its id, title, and overview
for res in search_result:
    print(res.id)
    print(res.title)
    print( res.poster_path)

    # print(res.overview)