from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import User
from backend.schemas import UserCreate, UserResponse
from backend.deps import get_current_admin
from backend.db import get_db
from passlib.context import CryptContext
from backend.crud import users as crud_users

pwd_context = CryptContext(schemes=["bcrypt"])

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)]  # 🔒 автоматически на всё
)

# CREATE USER
@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing = crud_users.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# READ USERS
@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# UPDATE ROLE
@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    db.commit()

    return {"message": "Role updated"}


# BLOCK USER
@router.put("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()

    return {"message": "User blocked"}


# UNBLOCK USER
@router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    return {"message": "User unblocked"}


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}