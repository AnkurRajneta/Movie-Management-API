# main.py
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.config.database import engine
from app.models import movie_model
from app.controller.movie_controller import router as movie_router
from app.controller.user_controller import router as user_router
from app.controller.auth_controller import router as auth_router
# from app.controller import auth_controller  # <— NEW

movie_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Management API", version="1.0.0")

# # Include routers
# app.include_router(auth_controller.router)  # root (/), /login, /logout
app.include_router(movie_router, prefix="/movies", tags=["Movies"])
app.include_router(user_router, prefix = "/user", tags =["User"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# templates = Jinja2Templates(directory="app/templates")
