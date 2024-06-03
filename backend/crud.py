import hashlib

from sqlalchemy.orm import Session

import backend.models as models
import backend.schemas as schemas


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
    books = db.query(models.Book).offset(skip).limit(limit).all()
    for book in books:
        if book.Rating:
            book.Rating = float(book.Rating[:-1])
        else:
            book.Rating = 0

        if not book.Description:
            book.Description = ''

    return books


def get_movies(db: Session, skip: int = 0, limit: int = 20):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    for movie in movies:
        if movie.rating:
            movie.rating = float(movie.rating.replace(",", "."))
        else:
            movie.rating = 0

        if not movie.description:
            movie.description = ""

    return movies
