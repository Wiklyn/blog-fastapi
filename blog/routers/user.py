from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..database import get_db
from ..repository import user
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post(
        "/",
        response_model=schemas.ShowUser,
        status_code=status.HTTP_200_OK
)
def create(request: schemas.User, db: Session = Depends(get_db)):

    return user.create(request, db)


@router.get(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=List[schemas.ShowUser]
)
def all(db: Session = Depends(get_db)):

    return user.get_all(db)


@router.get(
        "/{id}",
        status_code=status.HTTP_200_OK,
        response_model=schemas.ShowUser
)
def show(id, db: Session = Depends(get_db)):

    return user.get_one(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):

    return user.delete(id, db)
