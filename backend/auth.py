import hashlib
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import backend.crud as crud
from backend.schemas import UserCreate

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str


class TokenInner(BaseModel):
    accessToken: str


class Token(BaseModel):
    tokens: TokenInner


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    password_bytes = plain_password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    new_hashed_password = hash_object.hexdigest()
    return new_hashed_password == hashed_password


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def register_user(db: Session, user: UserCreate):
    user_from_db = crud.get_user_by_email(db, user.username)
    if user_from_db is not None:
        return False
    else:
        crud.create_user(db, user)
    return True
