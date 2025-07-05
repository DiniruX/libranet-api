from app.controllers.search import (
    get_books, get_users, get_libraries
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import core
from app.schemas.user import UserOut
from app.schemas.book import BookOut
from app.schemas.library import LibraryOut
from typing import List

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/books", response_model=List[BookOut])
def search_books(
    searchText: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(core.deps.get_db)
):
    return get_books(db, searchText, skip, limit)

@router.get("/users", response_model=List[UserOut])
def search_users(
    searchText: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(core.deps.get_db),
):
    return get_users(db, searchText, skip, limit)

@router.get("/libraries", response_model=List[LibraryOut])
def search_libraries(
    searchText: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(core.deps.get_db)
):
    return get_libraries(db, searchText, skip, limit)