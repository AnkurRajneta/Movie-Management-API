from pydantic import BaseModel

class movie_schema(BaseModel):
    name :str
    actors:int
    

    class Config:
        orm_mode = True
    
    

class movie_schema_2(movie_schema):
    id : int