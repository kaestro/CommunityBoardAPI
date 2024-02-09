from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...cache.cache_manager import CacheManager
from ...auth import get_current_user_email, get_user_session_and_id


class BoardCreate(BaseModel):
    name: str
    public: bool

router = APIRouter()

@router.post("/create")
def create_board(board: BoardCreate, user_email: str = Depends(get_current_user_email)):
    db_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 게시판 이름이 유일한지 확인
    if db_session.query(Board).filter_by(name=board.name).first() is not None:
        raise HTTPException(status_code=400, detail="Board name already exists")

    # 새 게시판 생성
    new_board = Board(name=board.name, public=board.public, user_id=user_id)
    db_session.add(new_board)
    db_session.commit()

    return {"message": "Board created successfully"}