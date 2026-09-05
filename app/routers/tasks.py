
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_404_NOT_FOUND
from app import models
from app.dependencies import get_current_user
from typing import List
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import HTTPException
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schemas
from fastapi import APIRouter
from app import crud
from app.limiter import limiter
from fastapi import Request
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model = List[schemas.TaskResponse])
@cache(expire = 30)
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)

async def clear_cache():
    await FastAPICache.clear()

@router.post("/", response_model = schemas.TaskResponse)
@limiter.limit("1/minute")
async def createTask(request: Request,task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_task = crud.get_task_by_title(task.title, db)
    if new_task:
        raise HTTPException(status_code = HTTP_400_BAD_REQUEST, detail = "task already exists")
    await clear_cache()
    return crud.create_task(task , current_user.id , db)


@router.get("/owner_id{owner_id}", response_model = List[schemas.TaskResponse])
def readTaskByOwnerId(owner_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if owner_id != current_user.id:
        raise HTTPException(status_code= HTTP_401_UNAUTHORIZED, detail= "unauthorized")
    
    return crud.get_task_by_owner_id(owner_id,db)

@router.get("/by_taskid{id}", response_model = schemas.TaskResponse)
def readTaskByTaskId(id: int, db: Session = Depends(get_db)):
   task = crud.get_task_by_id(id, db)

   if not task:
       raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = "task not found")
   return task

@router.get("/{title}", response_model = schemas.TaskResponse)
def readTaskByTitle(title: str, db: Session = Depends(get_db)):
   task = crud.get_task_by_title(title, db)

   if not task:
       raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = "task not found")
   return task


@router.put("/{id}", response_model = schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskReplace , db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    newtask = crud.get_task_by_id(task_id,db)

    if newtask.owner_id != current_user.id:
        raise HTTPException(status_code= HTTP_401_UNAUTHORIZED, detail= "unauthorized")

    if not newtask:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = "task not found")
    await clear_cache()
    return crud.update_task(task_id, task, db)

@router.delete("/{id}", response_model = schemas.TaskResponse)
async def deleteTask(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task_by_id(id, db)
    if not task:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = "task not found")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail = "unauthorised")

    crud.delete_task(id, db)
    await clear_cache()
    return task
    