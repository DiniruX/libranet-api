from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # admin, staff, customer

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    library_id: Optional[int]

    class Config:
        orm_mode = True