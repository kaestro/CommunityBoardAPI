from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...auth import get_current_user_email, get_user_session_and_id

router = APIRouter()

@router.get("/{board_id}")
def get_board(board_id: int, user_email: str = Depends(get_current_user_email)):
    db_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 본인이 생성하거나, 전체 공개된 게시판 조회
    board = db_session.query(Board).filter_by(id=board_id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    elif (board.user_id != user_id and not board.public):
        raise HTTPException(status_code=403, detail="Cannot access board not owned by user and not public")

    return {"id": board.id, "name": board.name, "public": board.public, "user_id": board.user_id}