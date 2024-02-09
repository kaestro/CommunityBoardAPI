from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...auth import get_current_user_email, get_user_session_and_id

class BoardDelete(BaseModel):
    id: int

router = APIRouter()

@router.delete("/delete")
def delete_board(board: BoardDelete, user_email: str = Depends(get_current_user_email)):
    db_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    # 유저가 소유한 게시판인지 확인
    target_board = db_session.query(Board).filter_by(id=board.id).first()
    if target_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if target_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete board not owned by user")

    # 게시판 삭제
    db_session.delete(target_board)
    db_session.commit()

    return {"message": "Board deleted successfully"}