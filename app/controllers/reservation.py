from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate


def create_reservation(db: Session, reservation: ReservationCreate):
    existing_reservation = db.query(Reservation).filter(
        Reservation.user_id == reservation.user_id,
        Reservation.library_id == reservation.library_id,
        # Checks if any book ID exists in the stored text
        Reservation.book_ids.ilike(f"%{reservation.book_ids[0]}%")
    ).first()
    if existing_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A reservation for this user, library, and book(s) already exists."
        )

    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    reservations = db.query(Reservation).offset(skip).limit(limit).all()
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")

    return reservations


def get_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found."
        )
    db_reservation.book_ids = db_reservation.book_ids.split(",")
    return db_reservation


def update_reservation(db: Session, reservation_id: int, reservation: ReservationCreate):
    db_reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found."
        )

    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)

    db.commit()
    db.refresh(db_reservation)
    db_reservation.book_ids = db_reservation.book_ids.split(",")
    return db_reservation


def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found."
        )

    db.delete(db_reservation)
    db.commit()
    return db_reservation


def get_user_reservations(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    reservations = db.query(Reservation).filter(
        Reservation.user_id == user_id).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reservations found for this user."
        )
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")
    return reservations


def get_library_reservations(db: Session, library_id: int, skip: int = 0, limit: int = 100):
    reservations = db.query(Reservation).filter(
        Reservation.library_id == library_id).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reservations found for this library."
        )
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")
    return reservations


def get_book_reservations(db: Session, book_id: int, skip: int = 0, limit: int = 100):
    reservations = db.query(Reservation).filter(
        Reservation.book_ids.contains([book_id])).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reservations found for this book."
        )
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")
    return reservations


def cancel_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found."
        )

    db_reservation.status = "cancelled"
    db.commit()
    db.refresh(db_reservation)
    db_reservation.book_ids = db_reservation.book_ids.split(",")
    return db_reservation


def confirm_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found."
        )

    db_reservation.status = "confirmed"
    db.commit()
    db.refresh(db_reservation)
    db_reservation.book_ids = db_reservation.book_ids.split(",")
    return db_reservation


def get_reservations_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    reservations = db.query(Reservation).filter(
        Reservation.status == status).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No reservations found with status '{status}'."
        )
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")
    return reservations


def get_reservations_by_date_range(db: Session, start_date: str, end_date: str, skip: int = 0, limit: int = 100):
    from sqlalchemy import and_
    reservations = db.query(Reservation).filter(
        and_(
            Reservation.reservation_from >= start_date,
            Reservation.reservation_to <= end_date
        )
    ).offset(skip).limit(limit).all()

    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reservations found in the specified date range."
        )
    for reservation in reservations:
        reservation.book_ids = reservation.book_ids.split(",")
    return reservations
