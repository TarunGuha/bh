from .task_base_enums import TaskBaseEnum


class TaskStatus(TaskBaseEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
