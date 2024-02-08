from fastapi import APIRouter, Depends, HTTPException, Header
from .cache.cache_manager import CacheManager

def get_session_id(session_id: str = Header(None)):
    print(session_id)
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session ID not found")
    return session_id

def get_current_user_email(session_id: str = Depends(get_session_id)) -> str:
    user_email = CacheManager().get(session_id)
    if user_email is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    return user_email