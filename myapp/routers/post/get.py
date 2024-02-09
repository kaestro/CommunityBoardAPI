from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email, get_user_session_and_id

router = APIRouter()

@router.get("/get/{post_id}")
def get_post(post_id: int, user_email: str = Depends(get_current_user_email)):
    database_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 본인이 생성하거나, 전체 공개된 게시판의 게시글인지 확인
    target_post = database_session.query(Post).filter_by(id=post_id).first()
    if target_post is None or (target_post.user_id != user_id and not target_post.board.public):
        raise HTTPException(status_code=403, detail="Cannot get post not owned by user and not public")

    # 게시글 조회
    return {"id": target_post.id, "title": target_post.title, "content": target_post.content}