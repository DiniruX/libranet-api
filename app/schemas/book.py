from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    library_id: int
    description: Optional[str] = None
    cover_image: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True