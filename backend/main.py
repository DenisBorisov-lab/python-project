import os.path
from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

import backend.auth as auth
import backend.crud as crud
import backend.models as models
import backend.schemas as schemas
from backend.database import SessionLocal, engine

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


async def get_current_user(authorization: Annotated[str, Header()], db: Session = Depends(get_db)):
    token = '' if 'Bearer' not in authorization else authorization.split('Bearer ')[-1]

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


@app.post("/api/auth/register")
async def register_user(req: schemas.UserCreate, db: Session = Depends(get_db)
                        ) -> auth.Token:
    access = auth.register_user(db, req)
    if access:
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": req.username}, expires_delta=access_token_expires
        )
        return auth.Token(tokens=auth.TokenInner(accessToken=access_token))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/api/auth/login")
async def login_for_access_token(
        req: schemas.UserCreate, db: Session = Depends(get_db)
) -> auth.Token:
    user = auth.authenticate_user(db, req.username, req.password)
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
    return auth.Token(tokens=auth.TokenInner(accessToken=access_token))


@app.get('/api/auth/me')
async def get_self_user(user=Depends(get_current_user)):
    return user


@app.get("/books")
async def get_books(skip: int = Query(0), db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip * 12, limit=12)


@app.get("/books/image")
async def get_books_image(name: str = Query(None)):
    p = f"./backend/images_books/{name}.jpg"
    if not os.path.exists(p):
        p = f"./backend/images_books/Этика.jpg"

    response = FileResponse(p)
    return response


@app.get("/recommendations/books")
async def get_recommendations_books(db: Session = Depends(get_db)):
    books = sorted(crud.get_books(db, skip=0, limit=500), key=lambda book: book.Rating, reverse=True)[:10]
    return books


@app.get("/movies")
async def get_movies(skip: int = Query(0), db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip * 12, limit=12)
    return movies


@app.get("/movies/image")
async def get_movies_image(name: str = Query(None)):
    p = f"./backend/images_films/{name}.jpg"
    if not os.path.exists(p):
        p = f"./backend/images_films/Человек-паук.jpg"

    response = FileResponse(p)
    return response


@app.get("/recommendations/movies")
async def get_recommendations_movies(db: Session = Depends(get_db)):
    movies = sorted(crud.get_movies(db, skip=0, limit=500), key=lambda movie: (movie.rating, hash(movie.release_date)),
                    reverse=True)[:10]
    return movies
