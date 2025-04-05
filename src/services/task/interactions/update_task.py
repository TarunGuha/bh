from datetime import datetime, timezone
from fastapi.exceptions import HTTPException

from services.task.models import Task
from services.task.params import UpdateTaskRequest


class UpdateTask:
    def __init__(self, db, request):
        self.db = db
        if isinstance(request, dict):
            self.request = UpdateTaskRequest(**request)
        elif isinstance(request, UpdateTaskRequest):
            self.request = request
        else:
            raise HTTPException(status_code=422, detail="Invalid request type")
        self.task = None
        self.response = None
        self.updateable_fields = ["title", "description", "status"]

    def get_task(self):
        self.task = (
            self.db.query(Task)
            .where(
                Task.id == self.request.id,
                Task.created_by == self.request.created_by,
                Task.deleted_at == None,
            )
            .first()
        )
        if not self.task:
            raise HTTPException(status_code=404, detail="No Task Found")

    def update_task(self):
        for key, value in self.request.model_dump(
            include=self.updateable_fields
        ).items():
            if value is not None:
                setattr(self.task, key, value)
        self.db.add(self.task)
        self.db.flush()

    def set_response(self):
        self.response = {
            "message": "Task Updated Successfully!",
            "task": self.task,
        }

    def execute(self):
        self.get_task()
        self.update_task()
        self.set_response()
        return self.response


def update_task(db, request):
    return UpdateTask(db, request).execute()
