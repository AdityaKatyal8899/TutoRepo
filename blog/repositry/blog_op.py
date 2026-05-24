from ..database import get_db
from .. import models, schema
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(db: Session, curr_user: models.User, blog: schema.Blog):
    new_blog = models.Blog(
        title=blog.title,
        body=blog.body,
        owner_id=curr_user.id
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def delete_blog(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail='blog not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return {"details": f"The blog with id: {id} is deleted successfully"}

def update_blog(id, request: schema.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    blog.update(
        {
            "title": request.title,
            "body": request.body
        },
        synchronize_session=False
    )

    db.commit()

    return {"message": f"Blog {id} updated successfully"}


def serve_blog(db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Not found")
    return blog