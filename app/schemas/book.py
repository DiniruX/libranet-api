from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    status: str = "available"
    floor: Optional[int] = None
    shelf: Optional[int] = None  
    library_id: int
    description: Optional[str] = None
    cover_image: Optional[str] = None

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
class BookOut(BookBase):
    id: int
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    status: str = "available"
    floor: Optional[int] = None
    shelf: Optional[int] = None
    library_id: int
    description: Optional[str] = None
    cover_image: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True