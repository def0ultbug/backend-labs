from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class Categories(str, Enum):
    DRAMA = "drama"
    FICTION = "fiction"
    NON_FICTION = "non_fiction"


class BookCreate(BaseModel):
    title: str = Field(..., min_length = 3,description="Title of the book")
    author : str = Field(...,description=" the author book") #TODO: make it a list because the book can have more then one
    price: float = Field(..., ge=0, description="Price of the book")
    stock_count: int = Field(..., ge=0, description="Number of books in stock")
    category: Categories = Field(..., description="Book category")

class Book(BookCreate):
    id: int = Field(..., description="Unique identifier of the book auto increamente")


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author : Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock_count: Optional[int] = Field(None, ge=0)
"""
b = BookUpdate(name = 'Jhon', price = 12)
for val in b.model_dump().values():
    print(val)
print(b.name)
"""