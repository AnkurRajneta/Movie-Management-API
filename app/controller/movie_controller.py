from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.service.movie_service import movie_service
from app.schema.movie_schema import movie_schema, movie_schema_2


# templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get('/Movies/Collections/1.1', response_model=List[movie_schema_2])
def get_movies(db: Session = Depends(get_db)):
    service = movie_service(db)
    return service.get_all_movies()


@router.post('/Movies/Collections/1.2', response_model=movie_schema_2)
def create_movies(movie: movie_schema, db: Session = Depends(get_db)):
    service = movie_service(db)
    return service.adding_movie(movie)


@router.put('/Movies/Collections/1.3/{movieid}', response_model=movie_schema_2)
def update_controller(movieid: int, movie: movie_schema, db: Session = Depends(get_db)):
    service = movie_service(db)
    updated = service.updating_movie_list(movieid, movie)
    if not updated:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    return updated


@router.delete("/Movies/1.4/{movieid}")
def delete_movie(movieid: int, db: Session = Depends(get_db)):
    service = movie_service(db)
    success = service.deleting_movie(movieid)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}


# @router.get('/dashboard')
# def dashboard(request: Request):
#     return templates.TemplateResponse("routes.html", {"request": request})
