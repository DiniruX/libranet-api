from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.book import Book
from app.schemas.book import BookCreate

def create_book(db: Session, book: dict):
    existing = db.query(Book).filter(Book.isbn == book["isbn"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    db_book = Book(**book)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: dict):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}