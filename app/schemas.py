from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    body : str
    published : bool

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at = datetime
    class Config:
        orm_mode=True


class CommentCreate(BaseModel):
    massage:str




class Post(PostBase):
    id:int
    created_at = datetime
    user_id:int
    owner : UserOut
    class Config:
        orm_mode=True


class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True


class CommentOut(BaseModel):
    id:int
    massage:str
    created_at: datetime
    post:Post
    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password : str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)