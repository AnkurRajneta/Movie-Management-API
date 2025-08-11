from concurrent.futures import ThreadPoolExecutor
from logging import config
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.service.movie_service import movie_service
from app.schema.movie_schema import movie_schema, movie_schema_2
import asyncio
from threading import Thread


# templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=3)
"Run async function in new thread to avoid blocking"

def background_insert(movie_data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _insert_movie_async():
        async with get_db() as db:
            service = movie_service(db)
            await service.insert_movies(movie_data)
        loop.run_until_complete(_insert_movie_async)
        loop.close()

@router.post("/insert")
async def insert_movies(movie:movie_schema, db:AsyncSession = Depends(get_db)):
    service = movie_service(db)
    inserted_movies = await service.insert_movies(movie)
    await db.commit()
    await db.refresh(inserted_movies)
    Thread(target=background_insert, args=(inserted_movies,), daemon=True).start()
    return inserted_movies

@router.get('', response_model=List[movie_schema_2])
async def get_movies(skip :int = Query(1, ge=0), limit : int = Query(2, le = 20),db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    return await service.get_all_movies(skip = skip, limit = limit)


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
