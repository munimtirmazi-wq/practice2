
from fastapi import Request
from pydantic import EmailStr
from starlette.status import HTTP_401_UNAUTHORIZED
from app.dependencies import get_current_user
from app import models
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND
from fastapi import HTTPException
from app import crud
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schemas
from fastapi import APIRouter
from app.limiter import limiter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model = schemas.UserResponse)
def getUserById(id:int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/byemail", response_model = schemas.UserResponse)
def getUserByEmail(email:EmailStr, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model = schemas.UserResponse)
@limiter.limit("1/minute")
def createUser(request: Request,user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_username(user.username, db)
    if new_user:
        raise HTTPException(status_code = HTTP_400_BAD_REQUEST, detail="Username already exists")
    new_user = crud.get_user_by_email(user.email, db)
    if new_user:
        raise HTTPException(status_code = HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user=crud.create_user(user, db)
    return new_user
        
@router.delete("/{id}")
def deleteUser(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if id==current_user.id:
        return crud.delete_user_by_id(id,db)

    raise HTTPException(status_code= HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    
    

    
