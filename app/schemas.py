from typing import Optional
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = Field(...,min_length=3, max_length=20)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=5, max_length=50)

class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str = Field(...,min_length=3, max_length=30)
    discription: Optional[str] = Field(None , max_length=100)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None,min_length=3, max_length=30)
    discription: Optional[str] = Field(None, max_length=100)
    completed: Optional[bool] = None


class TaskReplace(BaseModel):
    title: str = Field(None,min_length=3, max_length=30)
    discription: str = Field(None, max_length=100)
    completed: bool = None



class TaskResponse(TaskBase):
    id: int 
    completed: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None