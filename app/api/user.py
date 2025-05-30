from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import core
from app.schemas.user import User, UserCreate
from app.schemas.auth import LoginRequest
from app.models.user import User as UserModel
from app.core.deps import get_current_user
from app.controllers.user import create_user, get_users, get_user, update_user as update_user_controller, delete_user as delete_user_controller, user_login

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User)
def save_user(user: UserCreate, db: Session = Depends(core.deps.get_db)):
    return create_user(db, user)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(core.deps.get_db)):
    return user_login(db, email=payload.email, password=payload.password)


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return update_user_controller(db, user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return delete_user_controller(db, user_id)
