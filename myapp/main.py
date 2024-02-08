from fastapi import FastAPI
from .routers.user import signup, login, logout

app = FastAPI()

## 이후에는 이 라우터를 통합하는 방법을 찾아보자
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(logout.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}