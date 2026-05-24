from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import models, schema

# SECRET KEY (keep this secret!)
SECRET_KEY = "119d04e738db392ef5b62e7058eb580fcc82fb0a919e546385d2b9bc71007b76"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str, db, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")

        if email is None:
            raise credentials_exception
        
        token_data = schema.TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(email)).first()

    if user is None:
        raise credentials_exception
    
