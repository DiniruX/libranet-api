from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    dueDate = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="unpaid")  # unpaid, paid, cancelled
    amount = Column(String(255), nullable=True) 
    reason = Column(String(255), nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())