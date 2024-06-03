from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    ISBN: str
    Name: str
    page: str
    Age: str
    URL: str
    Genres: str
    Topic: str
    Rating: str
    Number_of_ratings: str
    Description: str
    Author: str
    Similars: str

    class Config:
        orm_mode = True
