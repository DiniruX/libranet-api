from app.models.book import Book
from app.models.user import User 
from app.models.library import Library
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_books(db: Session, searchText: str, skip: int = 0, limit: int = 100):
    results = db.query(Book).filter(
            Book.title.ilike(f"%{searchText}%") |
            Book.author.ilike(f"%{searchText}%") |
            Book.isbn.ilike(f"%{searchText}%") |
            Book.genre.ilike(f"%{searchText}%") |
            Book.status.ilike(f"%{searchText}%")
        ).offset(skip).limit(limit).all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found."
        )
    return results

def get_users(db: Session, searchText: str, skip: int = 0, limit: int = 100):
    users = db.query(User).filter(
        User.name.ilike(f"%{searchText}%") |
        User.email.ilike(f"%{searchText}%") |
        User.role.ilike(f"%{searchText}%")
    ).offset(skip).limit(limit).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found."
        )
    return users

def get_libraries(db: Session, searchText: str, skip: int = 0, limit: int = 100):
    libraries = db.query(Library).filter(
        Library.name.ilike(f"%{searchText}%") |
        Library.address.ilike(f"%{searchText}%") |
        Library.city.ilike(f"%{searchText}%")
    ).offset(skip).limit(limit).all()

    if not libraries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No libraries found."
        )
    return libraries