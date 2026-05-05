from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, index=True, nullable=False)
    vehicle_type = Column(String, nullable=False)
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    status = Column(String, default="parked")