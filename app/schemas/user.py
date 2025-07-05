from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # admin, staff, customer
    library_id: Optional[int] = None
    hashed_password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    library_id: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True