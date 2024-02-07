from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from ...database.db_manager import DatabaseManager

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    fullname: str
    email: str
    password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    db_manager = DatabaseManager()

    # Check if the email is already registered
    query = "SELECT * FROM users WHERE email=%s"
    params = (request.email,)  # 튜플로 파라미터 전달
    result = db_manager.execute_query(query, params)
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Insert the new user into the database
    query = "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)"
    params = (request.fullname, request.email, hashed_password)  # 튜플로 파라미터 전달
    db_manager.execute_query(query, params)

    return {"message": "User created successfully"}