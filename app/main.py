from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt 
from app.controller.movie_controller import router as movie_router
from app.controller.user_controller import router as user_router
from app.controller.auth_controller import router as auth_router
from app.dependencies.auth import get_current_user
from app.models import movie_model
from app.config.database import engine

movie_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Management API")

# Register routers
app.include_router(movie_router, prefix="/api/v1/movies", tags=["Movies"], dependencies=[Depends(get_current_user)])
app.include_router(user_router, prefix="/api/v1/user", tags=["User"], dependencies=[Depends(get_current_user)])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Welcome to Movie Management API"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Define Bearer token auth scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply BearerAuth globally (or restrict to some endpoints if preferred)
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
