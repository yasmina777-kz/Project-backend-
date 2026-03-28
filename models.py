from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey,Table, Text, DateTime
from db import Base


chat_members = Table(
    "chat_members",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chats.id")),
    Column("user_id", Integer, ForeignKey("users.id")))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="employee", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    posts: Mapped[list["Posts"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


    chats: Mapped[list["Chat"]] = relationship(
        "Chat",
        secondary=chat_members,
        back_populates="members"
    )

class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="posts")


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    members: Mapped[list["User"]] = relationship(
        "User",
        secondary=chat_members,
        back_populates="chats"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime)

    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    is_read = Column(Boolean, default=False)
    fike_url = Column(String, nullable=True)

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True)

    message_id = Column(Integer, ForeignKey("messages.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    emoji = Column(String)

