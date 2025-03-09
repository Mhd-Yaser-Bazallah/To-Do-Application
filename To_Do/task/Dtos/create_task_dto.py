from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    owner_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    completion_status:bool
    
    class Config:
        orm_mode = True