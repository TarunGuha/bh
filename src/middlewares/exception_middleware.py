import time
from uuid import uuid1
from typing import Final
from traceback import format_exc
from contextvars import ContextVar
from fastapi import Request, status
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import scoped_session, sessionmaker
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


from database.bh_db import engine as bh_engine


def get_path_template(request: Request) -> str:
    if hasattr(request, "path"):
        return ",".join(request.path.split("/")[1:])
    return ".".join(request.url.path.split("/")[1:])


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[str | None] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)

REQUEST_CTX_KEY: Final[str] = "request"
_request_ctx_var: ContextVar[Request | None] = ContextVar(REQUEST_CTX_KEY, default=None)


def get_request_id() -> str | None:
    return _request_id_ctx_var.get()


def get_request() -> Request | None:
    return _request_ctx_var.get()


def get_session():
    request = get_request()
    return request.state.db


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> StreamingResponse:
        try:

            ctx_token = None
            request_ctx_token = None

            request_id = str(uuid1())
            ctx_token = _request_id_ctx_var.set(request_id)
            request_ctx_token = _request_ctx_var.set(request)

            engine = bh_engine

            schema_engine = engine.execution_options(
                schema_translate_map={
                    None: "public",
                }
            )

            session = scoped_session(
                sessionmaker(bind=schema_engine), scopefunc=get_request_id
            )
            request.state.db = session()
            db_session_enabled = True
            request.state.db_session_enabled = True

            try:
                response = await call_next(request)
                # print("request state ->> ", request.state.__dict__)
                if request.method != "GET" and 200 <= response.status_code < 400:
                    if db_session_enabled:
                        request.state.db.flush()

                    if db_session_enabled:
                        request.state.db.commit()

                if response.status_code < 200 or response.status_code >= 400:
                    print(f"Rolling Back Status Code {request.url.path}, {response}")
                    if db_session_enabled:
                        request.state.db.rollback()

            except Exception as e:
                print(f"Rolling Back Error {request.url.path}, {e}")
                if request.method != "GET" and db_session_enabled:
                    request.state.db.rollback()
                # sentry_sdk.capture_exception(e)
                raise e from None
            finally:
                if db_session_enabled:
                    session.remove()

        except ValidationError as e:
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"success": False, "error": str(e), "traceback": format_exc()},
            )
        except ValueError as e:
            # sentry_sdk.capture_exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"success": False, "error": str(e), "traceback": format_exc()},
            )
        except HTTPException as e:
            # sentry_sdk.capture_exception(e)
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": str(e.detail),
                    "traceback": format_exc(),
                    "success": False,
                },
            )
        except Exception as e:
            # sentry_sdk.capture_exception(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "error": str(e), "traceback": format_exc()},
            )
        if ctx_token:
            _request_id_ctx_var.reset(ctx_token)
        if request_ctx_token:
            _request_ctx_var.reset(request_ctx_token)

        return response
