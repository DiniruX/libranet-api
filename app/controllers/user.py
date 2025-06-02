from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.utils.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.controllers.actionLog import create_action_log


def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    hashed_pw = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
        library_id=user.library_id,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user_created = db.query(User).filter(User.email == user.email).first()

    action_log = {
        "user_id": db_user_created.id,
        "action": f"Created user: {db_user_created.name}"
    }
    create_action_log(db, action_log)

    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: UserSchema, current_user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)

    action_log = {
        "user_id": current_user_id,
        "action": f"Updated user: {db_user.name}"
    }
    create_action_log(db, action_log)

    return db_user


def delete_user(db: Session, user_id: int, current_user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    if db_user:
        db.delete(db_user)
        db.commit()

    action_log = {
        "user_id": current_user_id,
        "action": f"Deleted user: {db_user.name}"
    }
    create_action_log(db, action_log)

    return db_user


def user_login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    token = create_access_token(data={"sub": str(user.id)})

    action_log = {
        "user_id": user.id,
        "action": f"User logged in: {user.name}"
    }
    create_action_log(db, action_log)

    print(f"User {user.name} logged in successfully.")

    return {"access_token": token, "token_type": "bearer", "user": user}

