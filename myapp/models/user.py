from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.db_manager import DatabaseManager


class User(DatabaseManager.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname= Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    boards = relationship("Board", back_populates="user")
    posts = relationship("Post", back_populates="user")