from sqlalchemy import Column, String, Boolean, Integer
from app.config.database import Base

class movie_model(Base):

    __tablename__ = "Films"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    actors = Column(Integer)
