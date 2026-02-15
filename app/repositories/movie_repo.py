from app.models import *
from app.db.db import *


class MovieRepository:
    def __init__(self) -> None:
        pass

    def add_movie(self, movie: Movies):
        movies[movie.id] = movie.model_dump()
        return True

    def remove_movie(self, movie_id: str):
        del movies[movie_id]
        return True

    def get_movie(self, movie_id: str):
        return movies[movie_id]

    def get_all_movies(self):
        return movies
