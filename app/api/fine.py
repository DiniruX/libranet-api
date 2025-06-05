from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import core
from app.schemas.fine import Fine, FineCreate
from app.models.user import User as UserModel
from app.core.deps import get_current_user
from app.controllers.fine import create_fine, get_fines, get_fine, get_fines_by_reservation_id, get_fines_by_status, update_fine as update_fine_controller, delete_fine as delete_fine_controller, mark_fine_as_cancelled as mark_fine_as_cancelled_controller, mark_fine_as_paid as mark_fine_as_paid_controller, auto_update_fine_amount as auto_update_fine_amount_controller, get_fines_by_lib_id

router = APIRouter(prefix="/fines", tags=["Fines"])


@router.post("/", response_model=Fine)
def save_fine(fine: FineCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return create_fine(db, fine, current_user.id)


@router.get("/", response_model=list[Fine])
def read_fines(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_fines(db, skip=skip, limit=limit)


@router.get("/{fine_id}", response_model=Fine)
def read_fine(fine_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_fine = get_fine(db, fine_id)
    if not db_fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return db_fine

@router.get("/library/{lib_id}", response_model=list[Fine])
def read_fines_by_library(lib_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_fines_by_lib_id(db, lib_id, skip=skip, limit=limit)


@router.put("/auto-update")
def auto_update_fine_amount(db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return auto_update_fine_amount_controller(db)


@router.get("/reservation/{reservation_id}", response_model=list[Fine])
def read_fines_by_reservation_id(reservation_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_fines_by_reservation_id(db, reservation_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=list[Fine])
def read_fines_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_fines_by_status(db, status, skip=skip, limit=limit)


@router.put("/{fine_id}", response_model=Fine)
def update_fine(fine_id: int, fine_data: FineCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return update_fine_controller(db, fine_id, fine_data, current_user.id)


@router.delete("/{fine_id}")
def delete_fine(fine_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return delete_fine_controller(db, fine_id, current_user.id)


@router.put("/{fine_id}/cancel")
def mark_fine_as_cancelled(fine_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return mark_fine_as_cancelled_controller(db, fine_id, current_user.id)


@router.put("/{fine_id}/pay")
def mark_fine_as_paid(fine_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return mark_fine_as_paid_controller(db, fine_id, current_user.id)
