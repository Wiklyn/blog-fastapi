from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..hashing import Hash


def create(request: schemas.User, db: Session):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all(db: Session):

    return db.query(models.User).all()


def get_one(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")

    return user


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")

    user.delete(synchronize_session=False)
    db.commit()

    return {"detail": f"User with id {id} successfully deleted."}
