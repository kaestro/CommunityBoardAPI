from fastapi import FastAPI
from .routers.account import signup, login

app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}