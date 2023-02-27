from fastapi import APIRouter, HTTPException, status, Depends
from app.database import Base, engine, get_db
from app import models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from app.oauth2 import get_current_user
from sqlalchemy import func


router = APIRouter(
    tags=['Comments']
)


@router.post('/comment/{post_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
async def create(post_id:int, comment:schemas.CommentCreate, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post available with id {post_id}")

    new_comment = models.Comment(user_id=current_user.id, post_id=post.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get('/')
async def read_all(db:Session=Depends(get_db)):
    comments = db.query(models.Comment).all()
    return comments


@router.put('/{comment_id}')
async def update(comment_id:int, request:schemas.CommentCreate, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    post_update = db.query(models.Comment).filter(models.Comment.id == comment_id)
    post = post_update.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post available with id {post_id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    post_update = request.dict()
    # post_update.update(request.dict())
    db.query(models.Comment).filter(models.Comment.id==comment_id).update(post_update)
    db.commit()
    return post_update


@router.delete('/{comment_id}')
async def destroy(comment_id:int, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id==comment_id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no comment available with id {comment_id}")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    db.delete(comment)
    db.commit()
    return {'msg':'Deleted'}