from starlette.staticfiles import StaticFiles

from routers import auth, users, posts
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from db import Base, engine
from db import SessionLocal
from routers.auth import admin_required, get_db
from passlib.context import CryptContext
from crud import users as crud_users
from fastapi.middleware.cors import CORSMiddleware
from db import engine
from models import Base
from routers import users,chats,messages
from websocket import (router as ws_router)
from routers import reactions, uploads

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РџР•Р Р’Р«Рњ, РґРѕ СЂРѕСѓС‚РµСЂРѕРІ
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

app.include_router(reactions.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(uploads.router)



pwd_context = CryptContext(schemes=["bcrypt"])

