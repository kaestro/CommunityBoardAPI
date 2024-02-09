from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import uuid

from ...database.db_manager import DatabaseManager
from ...cache.cache_manager import CacheManager
from ...models.user import User

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

## TODO
# 현재 token으로 사용하고 있는 session_id는 uuid를 통해
# 간편하게 생성하였지만, 보안성이 부족할 수 있다.
# 추후에 oauth2를 통해 token을 생성하도록 수정하여 보안성을 높일 수 있다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 비밀번호를 해시화하기 위한 helper class
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 사용자 인증을 위한 helper function
def authenticate_user(db_manager, email: str, password: str):
    session = db_manager.get_session()
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        return None
    if not pwd_context.verify(password, user.password):
        return False
    return user

# TODO
# 보안성이 모자랄 수 있어, 최초 로그인 시도시 다음과 같은 추가적인 보안성을 제공할 수 있다.
# 1. 로그인 시도 횟수 및 시간 제한
# 2. salt 사용
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session_id: str = Header(None)):
    db_manager = DatabaseManager()
    user = authenticate_user(db_manager, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    cache_manager = CacheManager()

    ## TODO
    # 현재 cache_manager를 통해 session_id를 저장하고 있는데,
    # 이 때문에 login 더블체크가 안되던 지점을 확인하고 수정.
    # 동일한 알고리즘을 통해 확인하던 다른 코드들 있는지 여부 확인 필요
    if session_id is not None and cache_manager.get(session_id).decode("utf-8") == user.email:
        print(f"cache_manager has successfully retrieved the session_id: {session_id} for the user email: {user.email}")
        raise HTTPException(status_code=400, detail="User is already logged in")
    else:
        session_id = str(uuid.uuid4())
        cache_manager.set(session_id, user.email)
        print(f"cache_manager has successfully set the session_id: {session_id} for the user email: {user.email}")
    
    return {"access_token": session_id, "token_type": "bearer"}