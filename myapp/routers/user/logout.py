from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from ...cache.cache_manager import CacheManager

router = APIRouter()
# TODO
# 추후에 토큰을 oauth2를 통해 생성했을 경우에 변경할 시작점
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 사용자의 access token을 검증한 뒤, 로그아웃 처리
# 로그아웃 처리는 access token을 삭제하는 것으로 한다
@router.post("/logout")
async def logout(session_id: str = Header(None)):
    cache_manager = CacheManager()
    user = cache_manager.get(session_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    cache_manager.delete(session_id)
    print(f"User {user} logged out")
    return {"detail": "Logged out"}