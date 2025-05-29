from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import core
from app.schemas.library import Library, LibraryCreate
from app.controllers.library import create_library, get_libraries, get_library, update_library as update_library_controller, delete_library as delete_library_controller

router = APIRouter(prefix="/libraries", tags=["Libraries"])

@router.post("/", response_model=Library)
def save_library(library: LibraryCreate, db: Session = Depends(core.deps.get_db)):
    return create_library(db, library)

@router.get("/", response_model=list[Library])
def read_libraries(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db)):
    return get_libraries(db, skip=skip, limit=limit)

@router.get("/{library_id}", response_model=Library)
def read_library(library_id: int, db: Session = Depends(core.deps.get_db)):
    db_library = get_library(db, library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library

@router.put("/{library_id}", response_model=Library)
def update_library(library_id: int, library: LibraryCreate, db: Session = Depends(core.deps.get_db)):
    return update_library_controller(db, library_id, library)

@router.delete("/{library_id}")
def delete_library(library_id: int, db: Session = Depends(core.deps.get_db)):
    return delete_library_controller(db, library_id)