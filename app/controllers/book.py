from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.book import Book
from app.schemas.book import BookCreate
from app.controllers.actionLog import create_action_log

def create_book(db: Session, book: dict, user_id: int):
    existing = db.query(Book).filter(Book.isbn == book["isbn"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    db_book = Book(**book)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    action_log = {
        "user_id": user_id,
        "action": f"Created book: {db_book.title}. ISBN: {db_book.isbn}",
    }
    create_action_log(db, action_log)

    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: dict, user_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    action_log = {
        "user_id": user_id,
        "action": f"Updated book: {db_book.title}. ISBN: {db_book.isbn}",
    }
    create_action_log(db, action_log)

    return db_book

def delete_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    action_log = {
        "user_id": user_id,
        "action": f"Deleted book: {db_book.title}. ISBN: {db_book.isbn}",
    }
    create_action_log(db, action_log)

    return {"detail": "Book deleted successfully"}