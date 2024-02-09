from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...auth import get_current_user_email, get_user_session_and_id

class BoardUpdate(BaseModel):
    id: int
    name: str
    public: bool

router = APIRouter()

@router.put("/update")
def update_board(board: BoardUpdate, user_email: str = Depends(get_current_user_email)):
    db_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 유저가 소유한 게시판인지 확인
    target_board = db_session.query(Board).filter_by(id=board.id).first()
    if target_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if target_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update board not owned by user")

    # 게시판 이름이 유일한지 확인
    if db_session.query(Board).filter(Board.name == board.name, Board.id != board.id).first() is not None:
        raise HTTPException(status_code=400, detail="Board name already exists")

    # 게시판 업데이트
    target_board.name = board.name
    target_board.public = board.public
    db_session.commit()

    return {"message": "Board updated successfully"}