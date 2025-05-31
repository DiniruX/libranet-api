from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.interLibReservations import interLibReservation
from app.schemas.interLibReservations import interLibReservationCreate

def create_inter_lib_reservation(db: Session, reservation: interLibReservationCreate):
    db_reservation = interLibReservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_inter_lib_reservations(db: Session, skip: int = 0, limit: int = 100):
    reservations = db.query(interLibReservation).offset(skip).limit(limit).all()
    return reservations

def get_inter_lib_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(interLibReservation).filter(
        interLibReservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inter-library reservation not found."
        )
    return db_reservation

def get_inter_lib_reservation_by_reservation_id(db: Session, reservation_id: int):
    db_reservation = db.query(interLibReservation).filter(
        interLibReservation.reservation_id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inter-library reservation not found."
        )
    return db_reservation

def update_inter_lib_reservation(db: Session, reservation_id: int, reservation: interLibReservationCreate):
    db_reservation = db.query(interLibReservation).filter(
        interLibReservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inter-library reservation not found."
        )

    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)

    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def delete_inter_lib_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(interLibReservation).filter(
        interLibReservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inter-library reservation not found."
        )

    db.delete(db_reservation)
    db.commit()
    return {"detail": "Inter-library reservation deleted successfully."}