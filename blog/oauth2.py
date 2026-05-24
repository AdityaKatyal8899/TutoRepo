from fastapi import Depends, status,HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from . import JWT_token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return JWT_token.verify_token(token, db, credentials_exception)

    