from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


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
