from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
# from sqlalchemy.orm import Session
from app.models.movie_model import MovieModel
from app.schema.movie_schema import movie_schema
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete

class movies_repository:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def get_all_movies(self, skip: int = 1, limit : int = 2):
         movies =( select(MovieModel).offset(skip).limit(limit)
         .order_by(MovieModel.id)
         )
         result = await self.db.execute(movies)
         return result.scalars().all()
    
    async def create(self, movie:movie_schema):
        new_movie = MovieModel(name = movie.name,actors = movie.actors)
        self.db.add(new_movie)
        await self.db.commit()
        await self.db.refresh(new_movie)
        return new_movie
    
    async def update(self, movieid:int,movie:movie_schema):
        update_movies = (
            sqlalchemy_update(MovieModel)
            .where(MovieModel.id == movieid)
            .values(**movie.model_dump())
        )
        # db_movie = select(MovieModel).where(MovieModel.id == movieid)
        
        await self.db.execute(update_movies)
        await self.db.commit()
        updated_values = await self.db.get(MovieModel, movieid)
        return updated_values
    

    async def delete(self, movieid:int):
        
        deleted_movies =( sqlalchemy_delete(MovieModel)
        .where(MovieModel.id == movieid))
        
       
        await self.db.execute(deleted_movies)
        await self.db.commit()
        return True