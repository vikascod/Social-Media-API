from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.oauth2 import create_access_token
from app import database, schemas, models
from app.utils import verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
async def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")

    access_token = create_access_token(data={'user_id':user.id})
    return {"access_token":access_token, 'token_type':'bearer'}