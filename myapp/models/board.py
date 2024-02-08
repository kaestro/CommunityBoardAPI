# board.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database.db_manager import DatabaseManager
from .post import Post

class Board(DatabaseManager.Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    public = Column(Boolean, nullable=False, default=False)
    # 게시판의 생성자 user_id
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to User
    user = relationship('User', back_populates='boards')

    # Relationship to Post
    posts = relationship('Post', back_populates='board')