from fastapi import APIRouter, Depends, HTTPException, status
from .. import schema, models
from ..database import get_db
from sqlalchemy.orm import Session, Relationship
from ..hahser import Hash

router = APIRouter(tags=['users'])



def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user

@router.post("/user", response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#To fetch a user by id
@router.get("/user/{id}", response_model = schema.ShowUser)
def server_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f'No user with id {id} is found ' )

    return user