from uuid import UUID
from typing import Optional
from pydantic import Field, model_validator
from typing_extensions import Annotated

from contexts import get_user_id

from services.task.params.task_base_params import TaskBaseModel
from services.task.enums import TaskStatus


class UpdateTaskRequest(TaskBaseModel):
    id: Annotated[UUID, Field(..., description="The ID of the task to update")]
    created_by: Annotated[
        UUID, Field(..., description="The ID of the user who created the task")
    ]
    title: Annotated[Optional[str], Field(default=None, min_length=1, max_length=255)]
    description: Annotated[
        Optional[str], Field(default=None, min_length=1, max_length=255)
    ]
    status: Annotated[Optional[TaskStatus], Field(default=None)]

    @model_validator(mode="before")
    def inject_created_by(cls, payload):
        payload["created_by"] = get_user_id()
        return payload
