from fastapi import APIRouter, HTTPException, status, Depends
from app.utils import hash
from app import models, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/signup/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create(user:schemas.UserCreate, db:Session=Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/')
def all_user(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def show(id:int, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No user available with id {id}")
    return user


@router.delete('/delete/{id}')
def destroy(id:int, db:Session=Depends(get_db), current_user:int= Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No user available with id {id}")
    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")
    db.delete(user)
    db.commit()
    return "Deleted"