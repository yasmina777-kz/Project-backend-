from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Reaction
from deps import get_current_user

router = APIRouter(prefix="/reactions", tags=["Reactions"])


@router.post("/reactions/{message_id}")
def add_reaction(message_id: int, emoji: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    reaction = Reaction(
        message_id=message_id,
        user_id=current_user.id,
        emoji=emoji
    )
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction

@router.get("/{message_id}")
def get_reactions(message_id: int, db: Session = Depends(get_db)):

    reactions = db.query(Reaction).filter(
        Reaction.message_id == message_id
    ).all()

    return reactions
