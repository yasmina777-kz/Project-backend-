from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PostCreate(BaseModel):
    title: str
    body: str


class PostResponse(BaseModel):
    id: int
    title: str
    body: str          # ← добавлено
    user_id: int

    model_config = ConfigDict(from_attributes=True)  # ← добавлено


class UserAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class ChatCreate(BaseModel):
    name: str

class ChatResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str