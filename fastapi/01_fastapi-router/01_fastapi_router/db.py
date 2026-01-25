# a dumb Database for testing
from schemas.Book import Book
from pydantic import BaseModel,Field


class DataBase(BaseModel):
    Books : dict[int,list[Book]] = Field(default_factory=dict)

db = DataBase()



