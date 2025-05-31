from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActionLogBase(BaseModel):
    user_id: str
    action: str

class ActionLogCreate(ActionLogBase):
    pass

class ActionLog(ActionLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True