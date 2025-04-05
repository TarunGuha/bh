from fastapi import FastAPI

from core.config import APP_CONFIGS
from middlewares import ExceptionMiddleware

from services.user import user_router

app = FastAPI(**APP_CONFIGS)

app.add_middleware(ExceptionMiddleware)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome To BH!"}


@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "ok"}


@app.get("/create-tables", tags=["Test"])
def create_tables():
    from database.create_tables import create_tables

    create_tables()
    return {"message": "Tables created successfully"}


app.include_router(user_router, prefix="/user", tags=["User"])
