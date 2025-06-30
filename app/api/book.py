from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app import core
from typing import List
from app.schemas.book import Book, BookCreate
from typing import Optional
from app.models.user import User as UserModel
from app.core.deps import get_current_user
from app.controllers.book import (
    create_book, get_books, get_book,
    update_book as update_book_controller,
    delete_book as delete_book_controller, get_books_by_library_id
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
async def save_book(
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    genre: Optional[str] = Form(None),
    status: str = Form("available"),
    floor: Optional[int] = Form(None),
    shelf: Optional[int] = Form(None),
    library_id: int = Form(...),
    description: Optional[str] = Form(None),
    cover_image: Optional[UploadFile] = File(None),
    db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)
):
    print(f"Received cover_image: {cover_image}")
    cover_image_base64 = None
    if cover_image:
        image_bytes = await cover_image.read()
        import base64
        cover_image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    book_data = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "genre": genre,
        "status": status,
        "floor": floor,
        "shelf": shelf,
        "description": description,
        "library_id": library_id,
        "cover_image": cover_image_base64,
    }

    return create_book(db, book_data, current_user.id)


@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/library/{library_id}", response_model=List[Book])
def read_books_by_library(library_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return get_books_by_library_id(db, library_id, skip=skip, limit=limit)

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: int, title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    genre: Optional[str] = Form(None),
    status: str = Form("available"),
    floor: Optional[int] = Form(None),
    shelf: Optional[int] = Form(None),
    library_id: int = Form(...),
    description: Optional[str] = Form(None),
    cover_image: Optional[UploadFile] = File(None),
    db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)
):
    cover_image_base64 = None
    if cover_image:
        image_bytes = await cover_image.read()
        import base64
        cover_image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    book_data = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "genre": genre,
        "status": status,
        "floor": floor,
        "shelf": shelf,
        "description": description,
        "library_id": library_id,
        "cover_image": cover_image_base64,
    }
    return update_book_controller(db, book_id, book_data, current_user.id)


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(core.deps.get_db), current_user: UserModel = Depends(get_current_user)):
    return delete_book_controller(db, book_id, current_user.id)
