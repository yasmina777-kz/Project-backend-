from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from backend import schemas
from backend.db import get_db
from backend.crud import posts as crud_posts
from backend.deps import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/create", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user)
                ):
    created = crud_posts.create_new_post(
        db=db,
        title=post.title,
        body=post.body,
        user_id=current_user.id,
    )
    return created


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts_for_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = crud_posts.get_posts_for_user(
        db=db,
        user_id=current_user.id
    )
    return result
