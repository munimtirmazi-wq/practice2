from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, nullable=False, index= True)
    email = Column(String, nullable=False, index=True)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean, default= True)

    tasks = relationship("Task", back_populates= "owner", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=False, index=True)
    discription = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    owner = relationship("User", back_populates= "tasks" )

