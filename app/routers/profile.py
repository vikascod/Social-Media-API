from fastapi import APIRouter, Depends, HTTPException, status
from app import models, schemas, database, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Profile'],
    prefix='/profile'
)


@router.post('/')
async def create_profile(profile:schemas.ProfileCreate, db:Session=Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if user_profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")
    new_profile = models.Profile(user_id=current_user.id, **profile.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.get('/{user_id}')
async def read_profile(user_id:int, db: Session = Depends(database.get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile not found for user {user_id}")
    return profile


@router.put('/{user_id}')
async def update_profile(user_id: int, request: schemas.ProfileCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    profile_update = db.query(models.Profile).filter(models.Profile.user_id == user_id)
    profile = profile_update.one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile not found with id {user_id}")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No Permission to perform action")
    profile_update.update(request.dict(exclude_unset=True))
    db.commit()
    return profile_update.one()


