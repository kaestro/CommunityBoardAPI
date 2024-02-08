from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...cache.cache_manager import CacheManager
from ...auth import get_current_user_email


class BoardCreate(BaseModel):
    name: str
    public: bool

router = APIRouter()

@router.post("/create")
def create_board(board: BoardCreate, user_email: str = Depends(get_current_user_email)):
    # 세션 확인
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    # 데이터베이스 세션 가져오기
    session = DatabaseManager().get_session()
    user_email = user_email.decode("utf-8")
    user_id = session.query(User).filter_by(email=user_email).first().id

    # 게시판 이름이 유일한지 확인
    if session.query(Board).filter_by(name=board.name).first() is not None:
        raise HTTPException(status_code=400, detail="Board name already exists")

    # 새 게시판 생성
    new_board = Board(name=board.name, public=board.public, user_id=user_id)
    session.add(new_board)
    session.commit()

    return {"message": "Board created successfully"}