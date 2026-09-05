from app.routers import tasks
from app.routers import auth
from app.routers import users
from fastapi import FastAPI
from app import models
from app.database import engine
from app.cache import init_cache

app = FastAPI(title="My Practice Task")

models.Base.metadata.create_all(bind = engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    init_cache()

@app.get("/")
def homePage():
    return {"message":"Welcome to my practice task"}

