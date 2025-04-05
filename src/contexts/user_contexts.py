from contextvars import ContextVar


user_id_ctx_var: ContextVar[str] = ContextVar("user_id", default=None)


def set_user_id(user_id: str):
    user_id_ctx_var.set(user_id)


def get_user_id() -> str:
    return user_id_ctx_var.get()
