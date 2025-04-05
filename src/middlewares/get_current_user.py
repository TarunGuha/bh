from uuid import UUID
from typing import Optional
from typing_extensions import Annotated
from fastapi import Header, HTTPException, status, Depends
from jwt import decode, ExpiredSignatureError, InvalidTokenError

from contexts import set_user_id
from core.config import JWT_PRIVATE_KEY


ALGORITHM = "ES256"


async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.split(" ")[1]

    try:
        payload = decode(token, JWT_PRIVATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    set_user_id(user_id)

    return user_id


CurrentUser = Annotated[Optional[UUID], Depends(get_current_user)]
