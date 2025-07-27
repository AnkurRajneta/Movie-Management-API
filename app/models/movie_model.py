from sqlalchemy import Column, String, Integer
from app.config.database import Base
from app.enums.table_enums import TableName

class MovieModel(Base):

    __tablename__ = TableName.MOVIE
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    actors = Column(Integer)
