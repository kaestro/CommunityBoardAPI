from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import uuid

from ...database.db_manager import DatabaseManager
from ...cache.cache_manager import CacheManager

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 비밀번호를 해시화하기 위한 helper class
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 사용자 인증을 위한 helper function
# 사용자가 입력한 이메일과 비밀번호를 검증하여 사용자 정보를 반환
# 이메일이 등록되어 있지 않으면 None을 반이
# 비밀번호가 일치하지 않으면 False를 반환
# 이메일과 비밀번호가 일치하면 사용자 정보를 반환
def authenticate_user(db_manager, email: str, password: str):
    # Check if the email is registered
    query = "SELECT * FROM users WHERE email=%s"
    params = (email,)  # 튜플로 파라미터 전달

    # [(6, 'developer', 'didme07@gmail.com', '$2b$12$.6THpSNydhEW5wkUCLhApOhJXUIEvz.CdWBjJRWMC5ucj5q3EG/LS')]
    # 형태로 반환됨. 형태에 대해서 수정 필요
    user = db_manager.execute_query(query, params)
    print(user)
    if user is None or len(user) == 0:
        return None
    if not pwd_context.verify(password, user[0][3]):
        return False
    return user[0]

# 사용자 정보를 기반으로 access token을 생성하고 이를 캐시 상에
# 저장해 로그인을 구현한 뒤, access token을 반환한다.
# access token은 사용자의 session ID로 사용된다.
# session ID가 이미 존재한다면, 기존 session ID를 반환한다.
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session_id: str = Header(None)):
    db_manager = DatabaseManager()
    user = authenticate_user(db_manager, form_data.username, form_data.password)
    # 이메일이 등록돼있지 않은 경우
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 비밀번호가 틀린 경우
    elif user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the cache manager
    cache_manager = CacheManager()
    
    # 이미 session ID가 존재하고, 이 session ID가 이메일과 일치하는 경우
    # 기존 session ID를 반환한다.
    if session_id is not None and cache_manager.get(session_id) == user[2]:
        print(f"cache_manager has successfully retrieved the session_id: {session_id} for the user email: {user[2]}")
    # session ID가 존재하지 않거나, 이메일과 일치하지 않는 경우
    # 새로운 session ID를 생성하고, 이를 캐시에 저장한다.
    # 이후 session ID를 반환한다.
    else:
        session_id = str(uuid.uuid4())
        cache_manager.set(session_id, user[2])
        print(f"cache_manager has successfully set the session_id: {session_id} for the user email: {user[2]}")
    
    # Return the session ID as the access token
    return {"access_token": session_id, "token_type": "bearer"}