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
def signup(request: SignupRequest):
    db_manager = DatabaseManager()

    # Check if the email is already registered
    result = db_manager.execute_query(f"SELECT * FROM users WHERE email='{request.email}'")
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Insert the new user into the database
    db_manager.execute_query(
        f"INSERT INTO users (fullname, email, password) VALUES ('{request.fullname}', '{request.email}', '{hashed_password}')"
    )

    return {"message": "User created successfully"}