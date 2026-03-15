from fastapi import APIRouter, Depends, HTTPException
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

@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()

    return {"status": "deleted"}

@router.get("/search")
def search_messages(query: str, db: Session = Depends(get_db)):

    messages = db.query(Message).filter(
        Message.content.ilike(f"%{query}%")
    ).all()

    return messages

@router.get("/unread")
def unread_messages(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    messages = db.query(Message).filter(
        Message.user_id != current_user.id,
        Message.is_read == False
    ).all()

    return messages

@router.put("/{message_id}/read")
def read_message(message_id: int, db: Session = Depends(get_db)):

    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.is_read = True

    db.commit()

    return {"status": "read"}

