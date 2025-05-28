from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/")
def root():
    return {"message": "LibraNet API is running"}

@router.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"message": "Database connection successful"}