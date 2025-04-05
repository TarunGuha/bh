import bcrypt

from sqlalchemy import select
from fastapi.exceptions import HTTPException

from core.config import PASSWORD_SALT

from database.bh_db import DbSession

from services.user.models import User
from services.user.params import CreateUserRequest


class CreateUser:
    def __init__(self, db, request):
        self.db = db
        if not isinstance(request, CreateUserRequest):
            self.request = CreateUserRequest(**request)
        else:
            self.request = request
        self.response = None

    def check_username_availability(self):
        existing_user = self.db.scalars(
            select(User).where(
                User.username == self.request.username, User.deleted_at.is_(None)
            )
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="This Username is already taken. Please choose another username.",
            )

    def get_hashed_password(self):
        binary_password = self.request.password.encode("utf-8")
        binary_salt = PASSWORD_SALT.encode("utf-8")
        binary_hashed_password = bcrypt.hashpw(binary_password, binary_salt)
        hashed_password = binary_hashed_password.decode("utf-8")
        return hashed_password

    def create_user(self):
        user = User(
            username=self.request.username,
            password=self.get_hashed_password(),
        )
        self.db.add(user)
        self.db.flush()
        self.response = {
            "message": "User created successfully",
            "user_id": str(user.id),
        }

    def execute(self):
        self.check_username_availability()
        self.create_user()
        return self.response


def create_user(db, request):
    return CreateUser(db, request).execute()
