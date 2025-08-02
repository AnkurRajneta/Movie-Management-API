from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.movies_repository import movies_repository
from app.schema.movie_schema import movie_schema

class movie_service:
    def __init__(self, db: AsyncSession):
        self.repo = movies_repository(db)
        self.db = db

    async def get_all_movies(self):
        return await self.repo.get_all_movies()
    
    async def adding_movie(self, movie: movie_schema):
        return await self.repo.create(movie)
    
    async def updating_movie_list(self, movieid: int, movie: movie_schema):
        return await self.repo.update(movieid, movie)
    
    async def deleting_movie(self, movieid: int):
        return await self.repo.delete(movieid)
