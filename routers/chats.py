from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Chat
from backend.schemas import ChatCreate, ChatResponse

router = APIRouter(prefix="/chats", tags=["Chats"])

# создать чат
@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = Chat(name=chat.name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# получить все чаты
@router.get("/", response_model=list[ChatResponse])
def get_chats(db: Session = Depends(get_db)):
    return db.query(Chat).all()