from fastapi import APIRouter, Depends, HTTPException, Header
from .cache.cache_manager import CacheManager
from typing import Tuple
from sqlalchemy.orm import Session

# 해당 요청이 들어올 경우, 세션 ID를 헤더에서 가져온다.
def get_session_id(session_id: str = Header(None)):
    print(session_id)
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session ID not found")
    return session_id

def get_current_user_email(session_id: str = Depends(get_session_id)) -> str:
    cache_manager = CacheManager()
    user_email = cache_manager.get(session_id)
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    
    cache_manager.extend_session(session_id)    

    return user_email


# email을 헤더에서 받아온 이후에, 데이터베이스에서 해당 email에 해당하는
# 유저의 세션과 id를 가져온다.
def get_user_session_and_id(user_email: str, DatabaseManager, User) -> Tuple[Session, str, int]:
    # 세션 확인
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    # 데이터베이스 세션 가져오기
    session = DatabaseManager().get_session()
    user_email = user_email.decode("utf-8")
    user = session.query(User).filter_by(email=user_email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    return session, user_email, user_id