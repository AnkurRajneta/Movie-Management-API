from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.service.movie_service import movie_service
from app.schema.movie_schema import movie_schema, movie_schema_2


# templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get('', response_model=List[movie_schema_2])
async def get_movies(db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    return await service.get_all_movies()


@router.post('', response_model=movie_schema_2)
async def create_movies(movie: movie_schema, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    return await  service.adding_movie(movie)


@router.put('/{movieid}', response_model=movie_schema_2)
async def update_controller(movieid: int, movie: movie_schema, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    updated = await service.updating_movie_list(movieid, movie)
    if not updated:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    return  updated


@router.delete("/{movieid}")
async def delete_movie(movieid: int, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    success = await service.deleting_movie(movieid)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return  {"message": "Movie deleted successfully"}


# @router.get('/dashboard')
# def dashboard(request: Request):
#     return templates.TemplateResponse("routes.html", {"request": request})
