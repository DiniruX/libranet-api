from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    library_id = Column(Integer, ForeignKey("libraries.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reservation_from = Column(DateTime(timezone=True), nullable=False)
    reservation_to = Column(DateTime(timezone=True), nullable=False) # 2 weeks from reservation_from
    book_ids = Column(Text, nullable=False)  # Comma-separated list of book IDs
    status = Column(String(50), default="pending")  # pending, confirmed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
