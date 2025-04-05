from uuid import UUID
from typing_extensions import Annotated
from datetime import datetime, timezone
from typing import Optional, Union, List
from pydantic import Field, model_validator
from fastapi import HTTPException, status

from services.task.enums import TaskStatus
from services.task.params.task_base_params import TaskBaseModel


def ensure_utc(dt: datetime | None) -> datetime:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class ListTasksRequest(TaskBaseModel):
    id: Annotated[Optional[Union[UUID, List[UUID]]], Field(default=None)]
    title: Annotated[Optional[Union[str, List[str]]], Field(default=None)]
    status: Annotated[Optional[Union[TaskStatus, List[TaskStatus]]], Field(default=None)]
    created_by: Annotated[UUID, Field(..., description="The User ID of the creator")]
    created_at_less_than: Annotated[Optional[datetime], Field(default=None)]
    created_at_greater_than: Annotated[Optional[datetime], Field(default=None)]
    updated_at_less_than: Annotated[Optional[datetime], Field(default=None)]
    updated_at_greater_than: Annotated[Optional[datetime], Field(default=None)]
    page_limit: Annotated[
        int,
        Field(
            default=10,
            ge=1,
        ),
    ]
    page_number: Annotated[
        int,
        Field(
            default=1,
            ge=1,
        ),
    ]
    sort_by: Annotated[str, Field(default="updated_at")]
    sort_order: Annotated[str, Field(default="desc")]

    @model_validator(mode="after")
    def validate_created_at_less_than(self):
        self.created_at_less_than = ensure_utc(self.created_at_less_than)
        self.created_at_greater_than = ensure_utc(self.created_at_greater_than)
        self.updated_at_less_than = ensure_utc(self.updated_at_less_than)
        self.updated_at_greater_than = ensure_utc(self.updated_at_greater_than)
        return self

    @model_validator(mode="after")
    def validate_sort_order(self):
        if self.sort_order not in ["asc", "desc"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid sort_order value",
            )
        return self
