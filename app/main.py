from fastapi import FastAPI
from app.config.database import engine
from app.config.config import Database
from app.models import movie_model
from app.controller import movie_controller

movie_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Management API",
    version="1.0.0"
    
)

app.include_router(movie_controller.router, prefix="/movies", tags=["Movies"])
