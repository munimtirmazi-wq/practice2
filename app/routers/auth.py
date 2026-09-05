from app.auth import generate_access_token
from starlette.status import HTTP_401_UNAUTHORIZED
from h11._abnf import status_code
from fastapi import status
from fastapi import HTTPException
from app.auth import verify_password
from app import crud
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import schemas
from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags= ["auth"])

@router.post("/login", response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(form_data.username, db)

    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password", headers = {"WWW-Authenticate":"Bearer"})

    access_token = generate_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type":"bearer"}

