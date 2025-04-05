import logging
from math import ceil
from fastapi import status
from sqlalchemy import select, func
from fastapi.exceptions import HTTPException


from services.task.models import Task
from services.task.params import ListTasksRequest


class ListTasks:
    def __init__(self, db, request):
        self.db = db
        self.filters = []
        self.total_count = None
        if isinstance(request, dict):
            self.request = ListTasksRequest(**request)
        elif isinstance(request, ListTasksRequest):
            self.request = request
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid request type",
            )

    def create_query(self):
        self.query = select(Task)
        self.filters = [
            Task.created_by == self.request.created_by,
            Task.deleted_at == None,
        ]

    def build_filters(self):

        if self.request.id:
            if isinstance(self.request.id, list):
                self.filters.append(Task.id.in_(self.request.id))
            else:
                self.filters.append(Task.id == self.request.id)
        if self.request.title:
            if isinstance(self.request.title, list):
                self.filters.append(Task.title.in_(self.request.title))
            else:
                self.filters.append(Task.title == self.request.title)
        if self.request.status:
            if isinstance(self.request.status, list):
                self.filters.append(Task.status.in_(self.request.status))
            else:
                self.filters.append(Task.status == self.request.status)
        if self.request.created_at_less_than:
            self.filters.append(Task.created_at < self.request.created_at_less_than)
        if self.request.created_at_greater_than:
            self.filters.append(Task.created_at > self.request.created_at_greater_than)
        if self.request.updated_at_less_than:
            self.filters.append(Task.updated_at < self.request.updated_at_less_than)
        if self.request.updated_at_greater_than:
            self.filters.append(Task.updated_at > self.request.updated_at_greater_than)
        self.query = self.query.filter(*self.filters)

    def get_total_count(self):
        self.total_count = self.db.query(func.count()).filter(*self.filters).scalar()

    def apply_sorting(self):
        if self.request.sort_by:
            if bool(getattr(Task, self.request.sort_by)):
                self.query = self.query.order_by(
                    getattr(
                        getattr(Task, self.request.sort_by), self.request.sort_order
                    )()
                )
            else:
                self.query = self.query.order_by(
                    getattr(getattr(Task, "updated_at"), self.request.sort_order)()
                )

    def apply_pagination(self):
        self.query = self.query.offset(
            (self.request.page_number - 1) * self.request.page_limit
        ).limit(self.request.page_limit)

    def fetch_records(self):
        self.records = self.db.execute(self.query).scalars().all()

    def set_response(self):
        self.response = {
            "current_count": len(self.records),
            "total_count": self.total_count,
            "page_number": self.request.page_number,
            "total_pages": ceil(self.total_count / self.request.page_limit),
            "page_limit": self.request.page_limit,
            "list": self.records,
        }

    def execute(self):
        self.create_query()
        self.build_filters()
        self.get_total_count()
        self.apply_pagination()
        self.fetch_records()
        self.set_response()
        return self.response


def list_tasks(db, request):
    return ListTasks(db, request).execute()
