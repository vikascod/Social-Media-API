from fastapi import APIRouter, Depends, HTTPException, status
from app import database, schemas, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/follow',
    tags=['Follow']
)


@router.post('/user/{follower_id}')
async def follow_view(follower_id:int, db:Session=Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    followed_id = current_user.id
    if follower_id == followed_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User can't follow itself")
    user_follow = db.query(models.Follow).filter(models.Follow.follower_id == follower_id).first()
    if user_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already been followed")
    follows = models.Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(follows)
    db.commit()
    db.refresh(follows)
    return "Followed"


@router.delete('/{followed_id}')
async def unfollow_user(followed_id:int, db:Session=Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    follow = db.query(models.Follow).filter_by(follower_id=current_user.id, followed_id=followed_id).first()
    if follow:
        db.delete(follow)
        db.commit()
        return "Unfollow"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="followed not found")


@router.get('/{user_id}')
def get_follower(user_id:int, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id==user_id)
    if user:
        followers = db.query(models.Follow).filter_by(follower_id=user_id).all()
        return [follow.__dict__ for follow in followers]
    else:
        raise HTTPException(status_code=404, detail="User not found")
