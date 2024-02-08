from fastapi import Depends, FastAPI
from .routers.user import signup, login, logout
from .routers.board import create
from .auth import get_current_user_email

app = FastAPI()

# 라우터 등록
# utils에서 router들을 한번에 등록해주는 util을 작성중
app.include_router(signup.router, prefix="/user")
app.include_router(login.router, prefix="/user")
app.include_router(logout.router, prefix="/user")

app.include_router(create.router, prefix="/board")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test_auth")
async def test_auth(user_email: str = Depends(get_current_user_email)):
    return {"user_email": user_email}