from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email, get_user_session_and_id

class PostUpdate(BaseModel):
    id: int
    title: str
    content: str

router = APIRouter()

@router.put("/update")
def update_post(post: PostUpdate, user_email: str = Depends(get_current_user_email)):
    database_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 본인이 생성한 게시글인지 확인
    target_post = database_session.query(Post).filter_by(id=post.id).first()
    if target_post is None or target_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update post not owned by user")

    # 게시글 수정
    target_post.title = post.title
    target_post.content = post.content
    database_session.commit()

    return {"message": "Post updated successfully"}