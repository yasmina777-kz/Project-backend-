from starlette.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
from models import Base
from routers import auth, admin, users, posts, chats, messages, reactions, uploads


from websocket import router as ws_router
from passlib.context import CryptContext
from models import Assignment, Submission, User, Posts, Chat, Message, Reaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(ws_router)
app.include_router(reactions.router)
app.include_router(uploads.router)




app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

pwd_context = CryptContext(schemes=["bcrypt"])