from sqlalchemy import Column, Integer, String

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Book(Base):
    __tablename__ = "books"

    ISBN = Column(String, nullable=True)
    Name = Column(String, nullable=True)
    page = Column(String, nullable=True)
    Age = Column(String, nullable=True)
    URL = Column(String, nullable=True, primary_key=True)
    Genres = Column(String, nullable=True)
    Topic = Column(String, nullable=True)
    Rating = Column(String, nullable=True)
    Number_of_ratings = Column(Integer, nullable=True)
    Description = Column(String, nullable=True)
    Author = Column(String, nullable=True)
    Similars = Column(String, nullable=True)


class Movie(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    runtime = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    rating = Column(String, nullable=True)
    number_of_ratings = Column(String, nullable=True)
    description = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    country = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    key_words = Column(String, nullable=True)
    similars = Column(String, nullable=True)
