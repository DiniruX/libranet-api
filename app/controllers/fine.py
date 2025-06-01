from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.fine import Fine
from app.schemas.fine import FineCreate
from app.controllers.actionLog import create_action_log

FIXED_FINE_AMOUNT_PER_DAY = 500


def create_fine(db: Session, fine: FineCreate, user_id: int):
    db_fine = Fine(**fine.dict())
    db.add(db_fine)
    db.commit()
    db.refresh(db_fine)

    action_log = {
        "user_id": user_id,
        "action": f"Created fine for reservation ID {db_fine.reservation_id} with reason {db_fine.reason}",
    }
    create_action_log(db, action_log)

    return db_fine


def get_fines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Fine).offset(skip).limit(limit).all()


def get_fine(db: Session, fine_id: int):
    db_fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not db_fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fine not found")
    return db_fine


def get_fines_by_reservation_id(db: Session, reservation_id: int, skip: int = 0, limit: int = 100):
    return db.query(Fine).filter(Fine.reservation_id == reservation_id).offset(skip).limit(limit).all()

def get_fines_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    valid_statuses = ["unpaid", "paid", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    return db.query(Fine).filter(Fine.status == status).offset(skip).limit(limit).all()

def update_fine(db: Session, fine_id: int, fine_data: FineCreate, user_id: int):
    db_fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not db_fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fine not found")

    for key, value in fine_data.dict().items():
        setattr(db_fine, key, value)

    db.commit()
    db.refresh(db_fine)

    action_log = {
        "user_id": user_id,
        "action": f"Updated fine ID {db_fine.id} with reason {db_fine.reason}",
    }
    create_action_log(db, action_log)

    return db_fine


def delete_fine(db: Session, fine_id: int, user_id: int):
    db_fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not db_fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fine not found")

    db.delete(db_fine)
    db.commit()

    action_log = {
        "user_id": user_id,
        "action": f"Deleted fine ID {db_fine.id}",
    }
    create_action_log(db, action_log)

    return {"detail": "Fine deleted successfully"}


def mark_fine_as_paid(db: Session, fine_id: int, user_id: int):
    db_fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not db_fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fine not found")

    db_fine.status = "paid"
    db.commit()
    db.refresh(db_fine)

    action_log = {
        "user_id": user_id,
        "action": f"Marked fine ID {db_fine.id} as paid",
    }
    create_action_log(db, action_log)

    return db_fine


def mark_fine_as_cancelled(db: Session, fine_id: int, user_id: int):
    db_fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not db_fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fine not found")

    db_fine.status = "cancelled"
    db.commit()
    db.refresh(db_fine)

    action_log = {
        "user_id": user_id,
        "action": f"Marked fine ID {db_fine.id} as cancelled",
    }
    create_action_log(db, action_log)

    return db_fine


def auto_update_fine_amount(db: Session):
    late_return_fines = db.query(Fine).filter(
        Fine.reason == 'late return',
        Fine.status != 'cancelled'
        ).all()
    
    current_date = datetime.now()
    
    for fine in late_return_fines:
        noOfDays = (current_date - fine.dueDate).days
        if noOfDays > 0:
            fine.amount = str(noOfDays * FIXED_FINE_AMOUNT_PER_DAY)
            fine.status = "unpaid"
            db.commit()
            db.refresh(fine)

    late_return_fines_count = len(late_return_fines)
    if late_return_fines_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No late return fines found"
        )
    
    return late_return_fines
