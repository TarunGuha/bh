from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Query
from typing import Union, Optional, List

from middlewares import CurrentUser
from database.bh_db import DbSession

from ..params import *
from ..interactions import *


task_router = APIRouter()


@task_router.post("/create-task")
def create_task_api(
    db: DbSession,
    request: CreateTaskRequest,
    current_user: CurrentUser,
):
    return create_task(db, request)


@task_router.get("/list-tasks")
def list_tasks_api(
    db: DbSession,
    created_by: CurrentUser,
    id: Optional[Union[UUID, List[UUID]]] = Query(default=None),
    title: Optional[Union[str, List[str]]] = Query(default=None),
    status: Optional[Union[str, List[str]]] = Query(default=None),
    created_at_less_than: Optional[datetime] = Query(default=None),
    created_at_greater_than: Optional[datetime] = Query(default=None),
    updated_at_less_than: Optional[datetime] = Query(default=None),
    updated_at_greater_than: Optional[datetime] = Query(default=None),
    page_limit: Optional[int] = Query(default=10),
    page_number: Optional[int] = Query(default=1),
    sort_by: Optional[str] = Query(default="updated_at"),
    sort_order: Optional[str] = Query(default="desc"),
):
    request = ListTasksRequest(
        id=id,
        title=title,
        status=status,
        created_by=created_by,
        created_at_less_than=created_at_less_than,
        created_at_greater_than=created_at_greater_than,
        updated_at_less_than=updated_at_less_than,
        updated_at_greater_than=updated_at_greater_than,
        page_limit=page_limit,
        page_number=page_number,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return list_tasks(db, request)


@task_router.patch("/update-task")
def update_task_api(
    db: DbSession,
    request: UpdateTaskRequest,
    current_user: CurrentUser,
):
    return update_task(db, request)


@task_router.delete("/delete-task")
def delete_task_api(
    db: DbSession,
    request: DeleteTaskRequest,
    current_user: CurrentUser,
):
    return delete_task(db, request)
