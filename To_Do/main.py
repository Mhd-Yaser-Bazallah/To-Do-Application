from fastapi import FastAPI
from task.controller import router as task_router
from user.event_listener import start_event_listener
from base import get_db_instance
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
     
    db_instance = get_db_instance()
    yield   
     
    db_instance.close()

app = FastAPI(lifespan=lifespan)
 

 
app.include_router(task_router)

 
start_event_listener()
