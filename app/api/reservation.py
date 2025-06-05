from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import core
from app.schemas.reservation import Reservation, ReservationCreate
from datetime import datetime
from app.models.user import User as UserModel
from app.core.deps import get_current_user
from app.controllers.reservation import create_reservation, get_reservations, get_reservation, update_reservation as update_reservation_controller, delete_reservation as delete_reservation_controller, get_book_reservations, get_user_reservations, get_library_reservations, get_reservations_by_date_range, get_reservations_by_status, cancel_reservation as cancel_reservation_controller, confirm_reservation as confirm_reservation_controller, expire_reservations, get_books_in_reservations_between_dates as get_books_in_reservations_between_dates_controller

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=Reservation)
def save_reservation(reservation: ReservationCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_reservation = create_reservation(db, reservation, current_user.id)
    db_reservation.book_ids = db_reservation.book_ids.split(
        ",")
    return db_reservation


@router.get("/date-range", response_model=list[Reservation])
def read_reservations_by_date_range(start_date: str, end_date: str, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    return get_reservations_by_date_range(db, start_date_dt, end_date_dt)


@router.put("/expire", response_model=list[Reservation])
def expire_reservations_endpoint(db: Session = Depends(core.deps.get_db)):
    return expire_reservations(db)


@router.get("/", response_model=list[Reservation])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_reservations(db, skip=skip, limit=limit)


@router.get("/{reservation_id}", response_model=Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_reservation = get_reservation(db, reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation


@router.put("/{reservation_id}", response_model=Reservation)
def update_reservation(reservation_id: int, reservation: ReservationCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return update_reservation_controller(db, reservation_id, reservation, current_user.id)


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return delete_reservation_controller(db, reservation_id, current_user.id)


@router.get("/book/{book_id}", response_model=list[Reservation])
def read_book_reservations(book_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_book_reservations(db, book_id)


@router.get("/user/{user_id}", response_model=list[Reservation])
def read_user_reservations(user_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_user_reservations(db, user_id)


@router.get("/library/{library_id}", response_model=list[Reservation])
def read_library_reservations(library_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_library_reservations(db, library_id)


@router.get("/status/{status}", response_model=list[Reservation])
def read_reservations_by_status(status: str, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_reservations_by_status(db, status)

@router.get("/books-in-reservations/{start_date}/{end_date}", response_model=list[int])
def get_books_in_reservations_between_dates(start_date: str, end_date: str, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    return get_books_in_reservations_between_dates_controller(db, start_date_dt, end_date_dt)


@router.put("/{reservation_id}/cancel", response_model=Reservation)
def cancel_reservation(reservation_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return cancel_reservation_controller(db, reservation_id, current_user.id)


@router.put("/{reservation_id}/confirm", response_model=Reservation)
def confirm_reservation(reservation_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return confirm_reservation_controller(db, reservation_id, current_user.id)
