from sqlalchemy.orm import Session
from app.repository.movies_repository import movies_repository
from app.schema.movie_schema import movie_schema

class movie_service:
    def __init__(self, db: Session):
        self.repo = movies_repository(db)

    def get_all_movies(self):
        return self.repo.get_all_movies()
    
    def adding_movie(self, movie: movie_schema):
        return self.repo.create(movie)
    
    def updating_movie_list(self, movieid: int, movie: movie_schema):
        return self.repo.update(movieid, movie)
    
    def deleting_movie(self, movieid: int):
        return self.repo.delete(movieid)
