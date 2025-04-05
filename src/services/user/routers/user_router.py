from fastapi import APIRouter

from database.bh_db import DbSession

from ..params import *
from ..interactions import *


user_router = APIRouter()


@user_router.post("/create-user")
async def create_user_api(db: DbSession, request: CreateUserRequest):
    return create_user(db, request)


@user_router.post("/login-user")
async def login_user_api(db: DbSession, request: LoginUserRequest):
    return login_user(db, request)
