from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import core
from app.schemas.interLibReservations import interLibReservation, interLibReservationCreate
from datetime import datetime
from app.models.user import User as UserModel
from app.core.deps import get_current_user
from app.controllers.interLibReservations import get_inter_lib_reservations, update_inter_lib_reservation, get_inter_lib_reservation

router = APIRouter(prefix="/inter-lib-reservations", tags=["Inter-Library Reservations"])

@router.get("/", response_model=list[interLibReservation])
def read_inter_lib_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_inter_lib_reservations(db, skip=skip, limit=limit)

@router.get("/{reservation_id}", response_model=interLibReservation)
def read_inter_lib_reservation(reservation_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_reservation = get_inter_lib_reservation(db, reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Inter-library reservation not found")
    return db_reservation

@router.put("/{reservation_id}", response_model=interLibReservation)
def update_inter_lib_reservation_endpoint(reservation_id: int, reservation: interLibReservationCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return update_inter_lib_reservation(db, reservation_id, reservation)