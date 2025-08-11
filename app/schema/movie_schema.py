from email import message
from pydantic import BaseModel
from typing import List

class movie_schema(BaseModel):
    name :str
    actors:int
    

    class Config:
        from_attributes=True
    
    

class movie_schema_2(movie_schema):
    id : int

class get_movie_schema(BaseModel):
      data : List[movie_schema_2]
      message: str
      status_code: int

class update_movie_schema(BaseModel):
     data: movie_schema_2
     message:str
     status_code: int
     
     error: str | None = None