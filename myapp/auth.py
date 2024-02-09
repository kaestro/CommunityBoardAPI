from fastapi import APIRouter, Depends, HTTPException, Header
from .cache.cache_manager import CacheManager

# 해당 요청이 들어올 경우, 세션 ID를 헤더에서 가져온다.
def get_session_id(session_id: str = Header(None)):
    print(session_id)
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session ID not found")
    return session_id

# 세션 id에 맞춰 email을 반환한다.
# 성공적으로 반환하면 세션 만료 시간을 연장한다.
def get_current_user_email(session_id: str = Depends(get_session_id)) -> str:
    cache_manager = CacheManager()
    user_email = cache_manager.get(session_id)
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    
    cache_manager.extend_session(session_id)    

    return user_email