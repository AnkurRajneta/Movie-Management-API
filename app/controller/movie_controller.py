from concurrent.futures import ThreadPoolExecutor
from logging import config
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, Query, Request,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.service.movie_service import movie_service
from app.schema.movie_schema import get_movie_schema, movie_schema, movie_schema_2, update_movie_schema
import asyncio
from threading import Thread
from app.dependencies.handler_response import create_response
from app.constants.response_messages import ResponseMessages

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
    # await db.commit()
    # await db.refresh(inserted_movies)
    Thread(target=background_insert, args=(inserted_movies,), daemon=True).start()
    return create_response(
        data = inserted_movies,
        message=ResponseMessages.Movies.INSERT_MOVIES,
        status_code=status.HTTP_200_OK

    )

@router.get('', response_model=get_movie_schema)
async def get_movies(skip :int = Query(1, ge=0), limit : int = Query(2, le = 20),db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    result = await service.get_all_movies(skip = skip, limit = limit)
    return create_response(
        data= result,
        message = ResponseMessages.Movies.GET_ALL_MOVIES,
        status_code = status.HTTP_200_OK
    )


@router.post('', response_model=movie_schema_2)
async def create_movies(movie: movie_schema, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    result =  await  service.adding_movie(movie)
    return create_response(
        data = result,
        message=ResponseMessages.Movies.CREATE_MOVIES,
        status_code=status.HTTP_200_OK
    )

@router.put('/{movieid}', response_model=update_movie_schema)
async def update_controller(movieid: int, movie: movie_schema, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    updated = await service.updating_movie_list(movieid, movie)
    movie_response = movie_schema_2.model_validate(updated)
    if not movie_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie Not Found")
    return  create_response(
        data = movie_response,
        message=ResponseMessages.Movies.UPDATED_MOVIES,
        status_code=status.HTTP_200_OK
    )


@router.delete("/{movieid}")
async def delete_movie(movieid: int, db: AsyncSession = Depends(get_db)):
    service = movie_service(db)
    success = await service.deleting_movie(movieid)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return  create_response(
        data = success,
        message = ResponseMessages.Movies.DELETED_MOVIES,
        status_code=status.HTTP_200_OK
    )


# @router.get('/dashboard')
# def dashboard(request: Request):
#     return templates.TemplateResponse("routes.html", {"request": request})
