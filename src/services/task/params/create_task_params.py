from uuid import UUID
from typing import Optional
from typing_extensions import Annotated
from pydantic import Field, model_validator

from contexts import get_user_id

from services.task.params.task_base_params import TaskBaseModel

from services.task.enums import TaskStatus


class CreateTaskRequest(TaskBaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255)]
    description: Annotated[
        Optional[str], Field(default=None, min_length=1, max_length=255)
    ]
    status: Annotated[Optional[TaskStatus], Field(default=TaskStatus.PENDING)]
    created_by: Annotated[UUID, Field(..., description="User Id Of The Logged In User")]

    @model_validator(mode="before")
    def inject_created_by(cls, payload):
        payload["created_by"] = get_user_id()
        return payload
