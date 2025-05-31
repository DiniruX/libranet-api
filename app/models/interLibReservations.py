from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class interLibReservation(Base):
    __tablename__ = "inter_lib_reservations"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    from_library_id = Column(Integer, ForeignKey("libraries.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, confirmed, declined
    logistic_status = Column(String(50), default="pending")  # pending, in_transit, delivered
    created_at = Column(DateTime(timezone=True), server_default=func.now())