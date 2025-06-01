from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FineBase(BaseModel):
    reservation_id: int
    dueDate: datetime
    status: str
    amount: str
    reason: str

class FineCreate(FineBase):
    pass

class Fine(FineBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True