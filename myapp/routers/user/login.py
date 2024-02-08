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
    
    if session_id is not None and cache_manager.get(session_id) == user.email:
        print(f"cache_manager has successfully retrieved the session_id: {session_id} for the user email: {user.email}")
    else:
        session_id = str(uuid.uuid4())
        cache_manager.set(session_id, user.email)
        print(f"cache_manager has successfully set the session_id: {session_id} for the user email: {user.email}")
    
    return {"access_token": session_id, "token_type": "bearer"}