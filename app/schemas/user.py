from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # admin, staff, customer
    library_id: Optional[int] = None

class UserCreate(UserBase):
    password: str
    pass

class User(UserBase):
    id: int
    is_active: bool
    library_id: Optional[int]

    class Config:
        orm_mode = True