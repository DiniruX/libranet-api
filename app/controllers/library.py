from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.library import Library
from app.schemas.library import LibraryCreate
from app.controllers.actionLog import create_action_log


def create_library(db: Session, library: LibraryCreate, user_id: int):
    existing_library = db.query(Library).filter(
        Library.name == library.name).first()
    if existing_library:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A library with this name already exists."
        )
    db_library = Library(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)

    # Create an action log entry for the library creation
    action_log = {
        "user_id": user_id,
        "action": f"Created library: {db_library.name}"
    }
    create_action_log(db, action_log)
    
    return db_library


def get_libraries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Library).offset(skip).limit(limit).all()


def get_library(db: Session, library_id: int):
    return db.query(Library).filter(Library.id == library_id).first()


def update_library(db: Session, library_id: int, library: LibraryCreate, user_id: int):
    db_library = db.query(Library).filter(Library.id == library_id).first()
    if db_library:
        for key, value in library.dict().items():
            setattr(db_library, key, value)
        db.commit()
        db.refresh(db_library)

    # Create an action log entry for the library creation
    action_log = {
        "user_id": user_id,
        "action": f"Updated library: {db_library.name}"
    }
    create_action_log(db, action_log)

    return db_library


def delete_library(db: Session, library_id: int, user_id: int):
    db_library = db.query(Library).filter(Library.id == library_id).first()
    if db_library:
        db.delete(db_library)
        db.commit()

    # Create an action log entry for the library creation
    action_log = {
        "user_id": user_id,
        "action": f"Deleted library: {db_library.name}"
    }
    create_action_log(db, action_log)

    return db_library
