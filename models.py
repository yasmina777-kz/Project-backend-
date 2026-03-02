from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String,default="employee", nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    posts: Mapped[list['Posts']] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
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