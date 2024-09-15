def check_movie_existence(movie_dataframe, movie_title):
    return movie_title in movie_dataframe.index