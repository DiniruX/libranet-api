from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    contact = Column(String(100))
    location = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())