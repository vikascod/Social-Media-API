from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    image_url = Column(String(300), nullable=True)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates='post')
    comment = relationship('Comment', back_populates='post')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post = relationship('Post', back_populates='owner')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))

    user = relationship("User")
    post = relationship("Post", back_populates='comment')

class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)


class Follow(Base):
    __tablename__ = 'follows'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

