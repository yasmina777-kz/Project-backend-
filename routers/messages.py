from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db
from schemas import MessageCreate
from deps import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/chat/{chat_id}")
def send_message(chat_id: int, msg: MessageCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        db.execute(
            text("INSERT INTO messages (content, chat_id, user_id) VALUES (:content, :chat_id, :user_id)"),
            {"content": msg.content, "chat_id": chat_id, "user_id": current_user.id}
        )
        db.commit()
        return {"status": "sent"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/{chat_id}")
def get_messages(chat_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT id, content, chat_id, user_id, created_at FROM messages WHERE chat_id = :cid ORDER BY id"),
            {"cid": chat_id}
        ).fetchall()
        return [
            {
                "id": r[0],
                "content": r[1],
                "chat_id": r[2],
                "user_id": r[3],
                "created_at": r[4].isoformat() if r[4] else None,
                "is_read": False,
                "fike_url": None
            }
            for r in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        result = db.execute(text("SELECT id FROM messages WHERE id = :id"), {"id": message_id}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Message not found")
        db.execute(text("DELETE FROM messages WHERE id = :id"), {"id": message_id})
        db.commit()
        return {"status": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_messages(query: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT id, content, chat_id, user_id, created_at FROM messages WHERE content ILIKE :q ORDER BY id"),
            {"q": f"%{query}%"}
        ).fetchall()
        return [{"id": r[0], "content": r[1], "chat_id": r[2], "user_id": r[3], "created_at": r[4].isoformat() if r[4] else None, "is_read": False, "fike_url": None} for r in result]
    except Exception:
        return []

@router.put("/{message_id}/read")
def read_message(message_id: int, db: Session = Depends(get_db)):
    return {"status": "read"}

@router.get("/unread")
def unread_messages(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return []