import uuid
from typing import List
from fastapi import status
from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, VARCHAR, JSONB
from sqlalchemy import func, DateTime, TEXT, ARRAY, Computed, select, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.bh_db import Base
from constants.global_constants import CURRENT_TIMESTAMP


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, index=True)
    password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=CURRENT_TIMESTAMP
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=CURRENT_TIMESTAMP,
        onupdate=CURRENT_TIMESTAMP,
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
