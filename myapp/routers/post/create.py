from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email, get_user_session_and_id

class PostCreate(BaseModel):
    board_id: int
    title: str
    content: str

router = APIRouter()

@router.post("/create")
def create_post(post: PostCreate, user_email: str = Depends(get_current_user_email)):
    database_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 본인이 조회할 수 있는 게시판인지 확인
    target_board = database_session.query(Board).filter_by(id=post.board_id).first()
    if target_board is None or (target_board.user_id != user_id and not target_board.public):
        raise HTTPException(status_code=403, detail="Cannot post to board not owned by user or not public")

    # 새 게시글 생성
    new_post = Post(board_id=post.board_id, title=post.title, content=post.content, user_id=user_id)
    database_session.add(new_post)
    database_session.commit()

    return {"message": "Post created successfully"}