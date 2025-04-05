from typing_extensions import Annotated
from fastapi.exceptions import HTTPException
from pydantic import Field, model_validator, StringConstraints

from .user_base_params import UserBaseModel


class CreateUserRequest(UserBaseModel):
    username: Annotated[
        str, StringConstraints(to_lower=True, min_length=1, max_length=20)
    ] = Field(default=..., description="Username")
    password: Annotated[str, StringConstraints(min_length=8, max_length=25)] = Field(
        default=..., description="Password"
    )

    @model_validator(mode="after")
    def validate_username(self):
        if len(self.username) < 1:
            raise HTTPException(
                status_code=400,
                detail="Username must be at least 1 character long.",
            )
        if len(self.username) > 20:
            raise HTTPException(
                status_code=400,
                detail="Username must be less than 20 characters long.",
            )
        valid_chars = "abcdefghijklmnopqrstuvwxyz._"
        for char in self.username:
            if char not in valid_chars:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid character in username: '{char}'.",
                )
        return self

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long.",
            )
        if len(self.password) > 25:
            raise HTTPException(
                status_code=400,
                detail="Password must be less than 25 characters long.",
            )
        if not any(char.isupper() for char in self.password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least one uppercase letter.",
            )
        if not any(char.islower() for char in self.password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least one lowercase letter.",
            )
        if not any(char.isdigit() for char in self.password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least one digit.",
            )
        if not any(char in "!@#$%^&*()_+-=|;:,.<>?~" for char in self.password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least one special character in the set !@#$%^&*()_+-=|;:,.<>?~",
            )
        return self
