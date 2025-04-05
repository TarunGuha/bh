from database.bh_db import Base, engine

from services.user.models import *


def create_tables():
    Base.metadata.create_all(bind=engine)
