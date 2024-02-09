from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email, get_user_session_and_id

router = APIRouter()

@router.get("/list/{board_id}")
def list_posts(board_id: int, limit: int = Query(10), offset: int = Query(0), user_email: str = Depends(get_current_user_email)):
    database_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 본인이 조회할 수 있는 게시판인지 확인
    target_board = database_session.query(Board).filter_by(id=board_id).first()
    if target_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    elif (target_board.user_id != user_id and not target_board.public):
        raise HTTPException(status_code=403, detail="Cannot list posts from board not owned by user and not public")

    # 게시글 목록 조회
    posts = database_session.query(Post).filter_by(board_id=board_id).all()

    # pagination 적용
    posts = posts[offset : offset + limit]

    return [{"id": post.id, "title": post.title, "content": post.content} for post in sorted(posts, key=lambda post: post.id)]