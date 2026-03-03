from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from backend.db import get_db
from backend.models import Message
from backend.schemas import MessageCreate
from backend.deps import get_current_user
from datetime import datetime


router = APIRouter(prefix="/messages", tags=["Messages"])

# отправить сообщение
@router.post("/chat/{chat_id}")
def send_message(chat_id: int, msg: MessageCreate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    message = Message(
        content=msg.content,
        chat_id=chat_id,
        user_id=current_user.id
    )
    db.add(message)
    db.commit()
    return {"status": "sent"}

# получить историю
@router.get("/chat/{chat_id}")
def get_messages(chat_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.chat_id == chat_id).all()