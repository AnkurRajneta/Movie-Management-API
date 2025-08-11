from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

def create_response(message:str, status_code: int = 200, data = None, error = None):
    return{
        "message":message,
        "status_code": status_code,
        "data" : data,
        "error": error
    }