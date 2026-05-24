from fastapi import APIRouter, Depends, HTTPException
from .. import schema, models, database
from sqlalchemy.orm import Session
from ..hahser import Hash
from ..JWT_token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['login'])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=404, detail= 'Invalid Credentials')
    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id)},   # subject = user identity
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }