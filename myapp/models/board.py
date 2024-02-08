# board.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    public = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to User
    user = relationship('User', back_populates='boards')

    # Relationship to Post
    posts = relationship('Post', back_populates='board')