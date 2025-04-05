from typing_extensions import Annotated
from pydantic import Field, StringConstraints


from .user_base_params import UserBaseModel


class LoginUserRequest(UserBaseModel):
    username: Annotated[
        str, StringConstraints(to_lower=True, min_length=1, max_length=20)
    ] = Field(default=..., description="Username")
    password: Annotated[str, StringConstraints(min_length=8, max_length=25)] = Field(
        default=..., description="Password"
    )
