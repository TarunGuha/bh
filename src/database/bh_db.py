import re
import time
import logging
import functools
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from core.config import BH_DATABASE_URL


logger = logging.getLogger(__name__)


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    f"{self.__class__} has incorrect attribute '{key}' in "
                    "__repr__attrs__".format
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = f"'{value}'"
            values.append(value if single else f"{key}:{value}")

        return " ".join(values)

    def __repr__(self):
        id_str = ("#" + self._id_str) if self._id_str else ""
        return "<{} {}{}>".format(
            self.__class__.__name__,
            id_str,
            " " + self._repr_attrs_str if self._repr_attrs_str else "",
        )


engine = create_engine(
    BH_DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base(cls=CustomBase)


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    if parameters:
        logger.debug(f"\n{cursor.mogrify(statement, parameters).decode('utf-8')}\n")
    else:
        logger.debug(f"\n{statement}\n")


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.info("Execution Time: %f", total)


def get_db(request: Request):
    return request.state.db


DbSession = Annotated[Session, Depends(get_db)]


def db_atomic(func):
    def wrapper(*args, **kwargs):
        db: Session = SessionLocal()
        try:
            resp = func(db, *args, **kwargs)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e from None
        finally:
            db.close()
        return resp

    return wrapper


def db_session(func):
    def wrapper(*args, **kwargs):
        with SessionLocal() as db:
            return func(db, *args, **kwargs)

    return wrapper


def resolve_table_name(name):
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


raise_attribute_error = object()


def resolve_attr(obj, attr, default=None):
    """Attempts to access attr via dotted notation, returns none if attr does not exist."""
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default
