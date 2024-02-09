from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email

router = APIRouter()

@router.get("/list")
def list_boards(limit: int = Query(10), offset: int = Query(0), user_email: str = Depends(get_current_user_email)):
    # 세션 확인
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    # 데이터베이스 세션 가져오기
    session = DatabaseManager().get_session()
    user_email = user_email.decode("utf-8")
    user_id = session.query(User).filter_by(email=user_email).first().id

    # 본인이 생성하거나, 전체 공개된 게시판 조회
    boards = session.query(Board).filter((Board.user_id == user_id) | (Board.public == True)).all()

    # board 목록을 해당 board에 작성된 post 개수 순으로 정렬
    # post 수가 같을 경우, board id 순으로 정렬
    boards = sorted(boards, key=lambda board: (-session.query(Post).filter_by(board_id=board.id).count(), board.id))

    # pagination 적용
    boards = boards[offset : offset + limit]

    return {"boards": [board.id for board in boards]}