from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

print(settings.database_username)

# To create tables on database using Model with SQLAlchemy
# models.Base.metadata.create_all(bind=engine) # it's not necessary with Alembic

app = FastAPI()

origins = ["*"] # public API ["*"] - specific ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,     # function that runs before ever request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}



