from app.auth import hashed_password
from app import models
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db





from app import schemas
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username==username).first()

def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email==email).first()

def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id==id).first()

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def delete_user_by_id(id:int, db: Session = Depends(get_db)):
    user = get_user_by_id(id, db)
    if not user:
        return None
    
    db.delete(user)
    db.commit()

def get_task_by_id(id: int , db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.id==id).first()

def get_task_by_owner_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.owner_id==id).all()

def get_task_by_title(title: str, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.title==title).first()

def get_all_tasks(db:Session = Depends(get_db)):
    return db.query(models.Task).all()

def create_task(task: schemas.TaskCreate, owner_id: int, db: Session = Depends(get_db)):
    new_task = models.Task(
        title = task.title,
        discription = task.discription,
        owner_id = owner_id,

    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(task_id:int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = get_task_by_id(task_id, db)

    if not db_task:
        return None
    
    update_data = task.model_dump(exclude_unset=True)

    for Field, Value in update_data.items():
        setattr(db_task, Field, Value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(task_id: int, db:Session = Depends(get_db)):
    db_task = get_task_by_id(task_id, db)
    if not db_task:
        return None

    db.delete(db_task)
    db.commit()
    return db_task