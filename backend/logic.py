from sqlalchemy.orm import Session
from .models import Car
from datetime import datetime

def get_stats(db: Session):
    """Отримує статистику парковки з бази даних."""
    on_parking = db.query(Car).filter(Car.status == "parked").count()
    total_visits = db.query(Car).count()
    return {
        "on_parking": on_parking,
        "total_visits": total_visits
    }

def get_all_cars(db: Session):
    """Отримує список усіх машин для фронтенду."""
    cars = db.query(Car).all()
    return [
        {
            "id": car.id,
            "plate_number": car.plate_number,
            "entry_time": car.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": car.status
        } for car in cars
    ]

def add_car(db: Session, plate_number: str):
    """Логіка додавання нової машини на парковку."""
    # Перевірка, чи стоїть машина на парковці
    existing_car = db.query(Car).filter(Car.plate_number == plate_number, Car.status == "parked").first()
    if existing_car:
        return None, "Машина вже на парковці"

    new_car = Car(plate_number=plate_number, status="parked")
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car, None