import logging
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from services.task.models import Task
from services.task.params import CreateTaskRequest


class CreateTask:
    def __init__(self, db, request):
        self.db = db
        self.task = None
        self.response = None
        if isinstance(request, dict):
            self.request = CreateTaskRequest(**request)
        elif isinstance(request, CreateTaskRequest):
            self.request = request
        else:
            raise HTTPException(
                status_code=422,
                detail="Request must be an instance of CreateTaskRequest",
            )

    def create_task(self):
        self.task = Task(
            title=self.request.title,
            description=self.request.description,
            status=self.request.status,
            created_by=self.request.created_by,
        )
        self.db.add(self.task)
        self.db.flush()

    def set_response(self):
        self.response = {
            "response": "Task created successfully",
            "data": jsonable_encoder(self.task),
        }

    def execute(self):
        self.create_task()
        self.set_response()
        return self.response


def create_task(db, request):
    return CreateTask(db, request).execute()
