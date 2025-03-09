from fastapi import HTTPException
from sqlalchemy.orm import Session
from task.models import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task):
        db_task = Task(**task.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_user_id(self, user_id: int):
        return self.db.query(Task).filter(Task.owner_id == user_id).all()
        
    def get_tasks(self, skip: int = 0, limit: int = 100):
        return self.db.query(Task).offset(skip).limit(limit).all()

    def update_task(self, task_id: int, task):
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int):
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
         
        if db_task is None:
            return None  

        self.db.delete(db_task)
        self.db.commit()
        
        return db_task