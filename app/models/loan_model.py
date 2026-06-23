from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime(timezone=True), nullable=True, default=None)
    status = Column(String(100), nullable=False)

    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")