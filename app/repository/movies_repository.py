from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
# from sqlalchemy.orm import Session
from app.models.movie_model import MovieModel
from app.schema.movie_schema import movie_schema

class movies_repository:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def get_all_movies(self):
         movies = select(MovieModel)
         result = await self.db.execute(movies)
         return result.scalars().all()
    
    async def create(self, movie:movie_schema):
        new_movie = MovieModel(name = movie.name,actors = movie.actors)
        self.db.add(new_movie)
        await self.db.commit()
        await self.db.refresh(new_movie)
        return new_movie
    
    async def update(self, movieid:int,movie:movie_schema):
        db_movie = select(MovieModel).where(MovieModel.id == movieid)
        result = await self.db.execute(db_movie)
        db_movie = result.scalars().first()

        if not db_movie:
            None

        db_movie.name = movie.name
        db_movie.actors = movie.actors
        await self.db.commit()
        await self.db.refresh(db_movie)
        return db_movie
    

    async def delete(self, movieid:int):
        db_movie = select(MovieModel).where(MovieModel.id == movieid)
        result = await self.db.execute(db_movie)
        db_movie = result.scalars().first()
        if not db_movie:
            return {"message": "unable to find what to delete"}
        
        await self.db.delete(db_movie)
        await self.db.commit()
        return True