from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from ...database.db_manager import DatabaseManager
from ...models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    fullname: str
    email: str
    password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    db_manager = DatabaseManager()
    session = db_manager.get_session()

    # Check if the email is already registered
    user = session.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(request.password)

    # Insert the new user into the database
    new_user = User(fullname=request.fullname, email=request.email, password=hashed_password)
    session.add(new_user)
    session.commit()

    return {"message": "User created successfully"}