from fastapi import FastAPI
from .routers.account import signup

app = FastAPI()

app.include_router(signup.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}