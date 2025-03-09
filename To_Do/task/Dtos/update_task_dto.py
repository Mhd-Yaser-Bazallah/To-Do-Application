from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str
    description: str
    completion_status:bool



    class Config:
        orm_mode = True    