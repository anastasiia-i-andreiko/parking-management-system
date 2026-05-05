from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    entry_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="parked") # 'parked' або 'left'