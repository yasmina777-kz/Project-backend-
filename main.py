from backend.routers import auth, users, posts
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import User
from backend.schemas import UserCreate, UserResponse
from backend.db import Base, engine
from backend.db import SessionLocal
from backend.routers.auth import admin_required, get_db
from passlib.context import CryptContext
from backend.crud import users as crud_users
from fastapi.middleware.cors import CORSMiddleware
from  backend.db import engine
from backend.models import Base
from backend.routers import users,chats,messages
from backend.websocket import (router as ws_router)


Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS должен быть ПЕРВЫМ, до роутеров
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)

app.include_router(chats.router)

app.include_router(messages.router)

app.include_router(ws_router)

pwd_context = CryptContext(schemes=["bcrypt"])
