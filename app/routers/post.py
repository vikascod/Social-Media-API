from fastapi import APIRouter, HTTPException, status, Depends
from app.database import Base, engine, get_db
from app import models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from app.oauth2 import get_current_user
from sqlalchemy import func


router = APIRouter(
    tags=['Posts'],
    prefix='/post'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create(post:schemas.PostCreate, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/', response_model=List[schemas.PostOut])
async def all_post(db:Session=Depends(get_db), current_user:int= Depends(get_current_user), limit:int=20, skip:int=0, search:Optional[str]=""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(models.Post.user_id ==current_user.id).all()

    return posts


@router.get('/{id}', response_model=schemas.PostOut)
async def show(id:int, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id==id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post available with id {id}")

    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id:int, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post available with id {id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    db.delete(post)
    db.commit()
    return {"msg":"Successfully Deleted"}



@router.put('/update/{id}')
async def update(id, request:schemas.PostCreate, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    post_update = db.query(models.Post).filter(models.Post.id==id)
    post = post_update.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post Found with id {id}')
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    post_update.update(request.dict())
    db.commit()
    return post_update.first()

