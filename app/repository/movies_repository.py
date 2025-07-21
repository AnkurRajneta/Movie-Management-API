from sqlalchemy.orm import Session
from app.models.movie_model import movie_model
from app.schema.movie_schema import movie_schema

class movies_repository:
    def __init__(self,db:Session):
        self.db = db

    def get_all_movies(self):
        return self.db.query(movie_model).all()
    
    def create(self, movie:movie_schema):
        new_movie = movie_model(name = movie.name,actors = movie.actors)
        self.db.add(new_movie)
        self.db.commit()
        self.db.refresh(new_movie)
        return new_movie
    
    def update(self, movieid:int,movie:movie_schema):
        db_movie = self.db.query(movie_model).filter(movieid == movie_model.id).first()
        db_movie.name = movie.name
        db_movie.actors = movie.actors
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie
    

    def delete(self, movieid:int):
        db_movie = self.db.query(movie_model).filter(movie_model.id == movieid).first()
        if not db_movie:
            return False
        self.db.delete(db_movie)
        self.db.commit()
        return True