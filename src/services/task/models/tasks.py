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

from services.task.enums import TaskStatus


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True, default=None, index=True
    )
    status: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False, default=TaskStatus.PENDING.value, index=True
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
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
