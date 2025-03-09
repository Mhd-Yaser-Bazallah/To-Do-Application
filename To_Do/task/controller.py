from fastapi import APIRouter, HTTPException
from .service import TaskService
from task.Dtos.create_task_dto import TaskCreate, TaskResponse
from task.Dtos.update_task_dto import TaskUpdate

router = APIRouter()  
task_service = TaskService()   

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    print("Received request to create task:", task)
    return task_service.create_task(task)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    db_task = task_service.get_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/user/{user_id}",response_model=list[TaskResponse])
def user_tasks(user_id: int):
    db_task = task_service.get_task_by_user_id(user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task



@router.get("/tasks/", response_model=list[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100):
    return task_service.get_tasks(skip, limit)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    db_task = task_service.update_task(task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db_task = task_service.delete_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task with ID {task_id} has been successfully deleted."}
