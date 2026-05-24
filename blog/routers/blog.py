from fastapi import APIRouter, Depends, HTTPException, status
from ..database import engine, SessionLocal, get_db
from .user import get_user
from .. import schema, models, oauth2
from ..repositry import blog_op
from sqlalchemy.orm import Session, Relationship
from typing import List

router = APIRouter(
    tags=['blogs']
    )


#To server all blogs 
@router.get("/blogs", response_model= List[schema.MetaBlog])
def server_all_blogs(db: Session = Depends(get_db), get_curr_user: schema.User = Depends(oauth2.get_current_user)):
    
    return blog_op.get_all(db)


#To create a new blog
@router.post("/blog", status_code=status.HTTP_201_CREATED )
def create_blog(blog: schema.Blog, db: Session = Depends(get_db), curr_user: models.User = Depends(get_user)):

    return blog_op.create_blog(db, curr_user, blog)


#To delete a blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(id, db: Session = Depends(get_db)):

    return blog_op.delete_blog(db, id)

   

#To put some changes on an exisiting blog
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schema.Blog, db: Session = Depends(get_db)):
    
    return blog_op.update_blog(id, request, db)


#To fetch a blog from DB
@router.get("/blog/{id}", status_code=200 , response_model=schema.MetaBlog)
def get_blog(id, db: Session = Depends(get_db)):

    return blog_op.serve_blog(db)

