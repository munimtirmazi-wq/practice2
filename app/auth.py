from typing import Optional
from datetime import timedelta
from datetime import datetime
from passlib.context import CryptContext
import bcrypt
from jose import JWTError, jwt


pwd_context = CryptContext(schemes="bcrypt")

def hashed_password(password: str):
    pwd_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_pwd, hashed_pwd):
    return bcrypt.checkpw(plain_pwd.encode("utf_8"),hashed_pwd.encode("utf-8"))

SECRET_KEY = "my name is munim tirmazi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None ):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
