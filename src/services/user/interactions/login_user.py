import jwt
import bcrypt
from fastapi import status
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta

from core.config import JWT_PRIVATE_KEY

from services.user.models import User
from services.user.params import LoginUserRequest


class LoginUser:
    def __init__(self, db, request):
        self.db = db
        self.user = None
        if not isinstance(request, LoginUserRequest):
            self.request = LoginUserRequest(**request)
        else:
            self.request = request
        self.response = None

    def get_user(self):
        self.user = self.db.scalars(
            select(User).where(
                User.username == self.request.username, User.deleted_at.is_(None)
            )
        ).first()
        if not self.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

    def verify_credential(self):
        binary_input_password = self.request.password.encode("utf-8")
        binary_stored_hashed_password = self.user.password.encode("utf-8")
        verified = bcrypt.checkpw(binary_input_password, binary_stored_hashed_password)
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

    def generate_token(self):
        payload = {
            "user_id": str(self.user.id),
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
        }
        token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm="ES256")
        self.response = {"bearer_token": token}

    def execute(self):
        self.get_user()
        self.verify_credential()
        self.generate_token()
        return self.response


def login_user(db, request):
    return LoginUser(db, request).execute()
