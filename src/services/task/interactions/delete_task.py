from fastapi import status
from datetime import datetime, timezone
from fastapi.exceptions import HTTPException

from services.task.models import Task
from services.task.params import DeleteTaskRequest


class DeleteTask:
    def __init__(self, db, request):
        self.db = db
        if isinstance(request, dict):
            self.request = DeleteTaskRequest(**request)
        elif isinstance(request, DeleteTaskRequest):
            self.request = request
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid request type",
            )
        self.task = None
        self.response = None

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

    def delete_task(self):
        self.task.deleted_at = datetime.now(timezone.utc)
        self.db.add(self.task)
        self.db.flush()

    def set_response(self):
        self.response = {
            "message": "Task deleted successfully",
            "task": self.task,
        }

    def execute(self):
        self.get_task()
        self.delete_task()
        self.set_response()
        return self.response


def delete_task(db, request):
    return DeleteTask(db, request).execute()
