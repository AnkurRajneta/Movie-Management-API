from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config.config import Database



engine = create_async_engine(Database, echo = True)





async_session_maker = async_sessionmaker(autoflush=False, expire_on_commit="False", class_=AsyncSession,bind = engine)

Base  = declarative_base()




async def get_db():
    async with async_session_maker() as session:
        yield session