from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class interLibReservationBase(BaseModel):
    reservation_id: int
    from_library_id: int
    status: str 
    logistic_status: str

class interLibReservationCreate(interLibReservationBase):
    pass

class interLibReservation(interLibReservationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True