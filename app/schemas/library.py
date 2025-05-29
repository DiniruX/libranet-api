from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LibraryBase(BaseModel):
    name: str
    city: str
    address: str
    location: str
    contact: Optional[str] = None

class LibraryCreate(LibraryBase):
    pass

class Library(LibraryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True