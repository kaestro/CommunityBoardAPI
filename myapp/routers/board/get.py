from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...auth import get_current_user_email

router = APIRouter()

@router.get("/{board_id}")
def get_board(board_id: int, user_email: str = Depends(get_current_user_email)):
    # 세션 확인
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    # 데이터베이스 세션 가져오기
    session = DatabaseManager().get_session()
    user_email = user_email.decode("utf-8")
    user_id = session.query(User).filter_by(email=user_email).first().id

    # 본인이 생성하거나, 전체 공개된 게시판 조회
    board = session.query(Board).filter_by(id=board_id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    elif (board.user_id != user_id and not board.public):
        raise HTTPException(status_code=403, detail="Cannot access board not owned by user and not public")

    return {"id": board.id, "name": board.name, "public": board.public, "user_id": board.user_id}