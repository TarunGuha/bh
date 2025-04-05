from uuid import UUID
from pydantic import Field, model_validator
from typing_extensions import Annotated

from contexts import get_user_id

from services.task.params.task_base_params import TaskBaseModel


class DeleteTaskRequest(TaskBaseModel):
    id: Annotated[UUID, Field(..., description="The ID of the task to delete")]
    created_by: Annotated[
        UUID, Field(..., description="The ID of the user who created the task")
    ]

    @model_validator(mode="before")
    def inject_created_by(cls, payload):
        payload["created_by"] = get_user_id()
        return payload
