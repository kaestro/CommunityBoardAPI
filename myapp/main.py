from fastapi import Depends, FastAPI
from .routers.user import signup, login, logout
from .routers.board import create as board_create, update as board_update, delete as board_delete, list as board_list, get as board_get
from .routers.post import create as post_create, update as post_update, delete as post_delete, get as post_get, list as post_list
from .auth import get_current_user_email

app = FastAPI()

# 라우터 등록
# TODO: utils에서 router들을 한번에 등록해주는 util을 작성한다.
app.include_router(signup.router, prefix="/user")
app.include_router(login.router, prefix="/user")
app.include_router(logout.router, prefix="/user")

app.include_router(board_create.router, prefix="/board")
app.include_router(board_update.router, prefix="/board")
app.include_router(board_delete.router, prefix="/board")
app.include_router(board_list.router, prefix="/board")
app.include_router(board_get.router, prefix="/board")

app.include_router(post_create.router, prefix="/post")
app.include_router(post_update.router, prefix="/post")
app.include_router(post_delete.router, prefix="/post")
app.include_router(post_get.router, prefix="/post")
app.include_router(post_list.router, prefix="/post")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test_auth")
async def test_auth(user_email: str = Depends(get_current_user_email)):
    return {"user_email": user_email}