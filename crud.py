from sqlalchemy.orm import Session
import hashlib

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password_bytes = user.password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    hashed_password = hash_object.hexdigest()

    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_books(db: Session, skip: int = 0, limit: int = 20):
    books = db.query(models.Book).offset(0).limit(limit).all()
    for book in books:
        book.Rating = round(float(book.Rating[:-1]))
    return books