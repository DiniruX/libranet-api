from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(50), unique=True, nullable=False)
    genre = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="available")  # e.g., available, checked_out, reserved, damaged, lost
    floor = Column(Integer, nullable=True)  
    shelf = Column(Integer, nullable=True)
    library_id = Column(Integer, ForeignKey("libraries.id"), nullable=False)
    description = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())