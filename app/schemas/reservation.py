from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReservationBase(BaseModel):
    library_id: int
    user_id: int
    reservation_from: datetime
    reservation_to: datetime
    book_ids: List[int] 
    status: str 
    from_library_id: Optional[int] = None  # For inter-library reservations

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True