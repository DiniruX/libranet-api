from pydantic import BaseModel, EmailStr
from typing import Optional

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

    class Config:
        orm_mode = True