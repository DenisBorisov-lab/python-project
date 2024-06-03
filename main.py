from sqlalchemy.orm import Session

from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError
import crud, models, schemas, auth
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(auth.oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[auth.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/register")
async def register_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
                        ) -> auth.Token:
    access = auth.register_user(db, form_data)
    if access:
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return auth.Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> auth.Token:
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=auth.User)
async def read_users_me(
        current_user: Annotated[auth.User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/recommendations")
async def get_books(db: Session = Depends(get_db)):
    books = sorted(crud.get_books(db, skip=0, limit=500), key=lambda book: book.Rating, reverse=True)
    return books


@app.get("/books")
async def get_recommendations(skip: int = Query(0), db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip * 20, limit=12)


@app.get("/books/image")
async def get_books_image(name: str = Query(None)):
    response = FileResponse(f"./imagine_books/{name}.jpg")
    return response


@app.get("/movies/image")
async def get_movies_image(name: str = Query(None)):
    response = FileResponse(f'')
    return response


@app.get("/movies")
async def get_movies(skip: int = Query(0), db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip * 20, limit=12)
    return movies
