from .repositories  import TaskRepository
from .Dtos.create_task_dto import TaskCreate
from .Dtos.update_task_dto import TaskUpdate
from base import get_db_instance

class TaskService:
    def __init__(self):
        self.db = get_db_instance()    
        self.task_repo = TaskRepository(self.db)

    def create_task(self, task: TaskCreate):
        return self.task_repo.create_task(task)

    def get_task(self, task_id: int):
        return self.task_repo.get_task(task_id)

    def get_task_by_user_id(self, user_id: int):
        return self.task_repo.get_tasks_by_user_id(user_id)

    def get_tasks(self, skip: int = 0, limit: int = 100):
        return self.task_repo.get_tasks(skip, limit)

    def update_task(self, task_id: int, task: TaskUpdate):
        return self.task_repo.update_task(task_id, task)

    def delete_task(self, task_id: int):
        return self.task_repo.delete_task(task_id)
