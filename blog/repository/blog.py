from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import models, schemas


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def get_all(db: Session):
    return db.query(models.Blog).all()


def get_one(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not available")

    return blog


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found.")

    blog.update(request.dict())
    db.commit()

    return f"Blog with id {id} successfully updated"


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found.")

    blog.delete(synchronize_session=False)
    db.commit()

    return {"detail": f"Blog with id {id} successfully deleted."}
