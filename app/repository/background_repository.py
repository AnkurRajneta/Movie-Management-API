import uuid
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.movie_model import MovieModel
from app.schema.movie_schema import movie_schema
from app.repository.movies_repository import movies_repository


class BackgroundRepository:
    def __init__(self, db : AsyncSession):
        self.db = db
        self.movie = movies_repository(db)

    async def create_background_data(self, payload:movie_schema):
          return await self.movie.create(payload)
