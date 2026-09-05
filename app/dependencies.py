
from app import crud
from app.auth import decode_access_token
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer


oauth2_scheme= OAuth2PasswordBearer(tokenUrl= "/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exception = HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail = "Unauthorized")

    payload = decode_access_token(token)

    if not payload:
        raise exception

    username = payload.get("sub")
    if not username:
        raise exception

    user = crud.get_user_by_username(username,db)
    if not user:
        raise exception
    return user