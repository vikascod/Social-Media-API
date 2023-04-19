from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    body : str
    image_url:str
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
    message:str




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


class ProfileCreate(BaseModel):
    first_name:str
    last_name:str
    profile_pic_url:str
    bio:str
    social_link:str

class Profile(ProfileCreate):
    id:int
    user_id:int
    created_on:datetime
    class Config:
        orm_mode=True


class UserLogin(BaseModel):
    email:EmailStr
    password : str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id: Union[int, None] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)


class FollowAdd(BaseModel):
    follower_id: int
    followed_id: int
    