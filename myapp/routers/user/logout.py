from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ...cache.cache_manager import CacheManager

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 사용자의 access token을 검증한 뒤, 로그아웃 처리
# 로그아웃 처리는 access token을 삭제하는 것으로 한다
@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    cache_manager = CacheManager()
    user = cache_manager.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    cache_manager.delete(token)
    print(f"User {user} logged out")
    return {"detail": "Logged out"}