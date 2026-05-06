import re
from sqlalchemy.orm import Session
from models import Car
from datetime import datetime


def validate_plate(plate_number: str):
    pattern = r"^[A-Z0-9]{3,10}$"
    return re.match(pattern, plate_number.upper()) is not None


def add_car(db: Session, plate_number: str, vehicle_type: str):
    if not validate_plate(plate_number):
        return None, "Невірний номер"

    active = db.query(Car).filter(
        Car.plate_number == plate_number.upper(),
        Car.status == "parked"
    ).first()

    if active:
        return None, "Авто вже на парковці"

    car = Car(
        plate_number=plate_number.upper(),
        vehicle_type=vehicle_type
    )

    db.add(car)
    db.commit()
    db.refresh(car)

    return car, None


def mark_exit(db: Session, car_id: int):
    car = db.query(Car).filter(
        Car.id == car_id,
        Car.status == "parked"
    ).first()

    if not car:
        return False

    car.status = "left"
    car.exit_time = datetime.utcnow()

    db.commit()
    return True


def get_filtered_cars(db: Session, search: str = None):
    query = db.query(Car)

    if search:
        query = query.filter(Car.plate_number.contains(search.upper()))

    return query.order_by(
        Car.status.desc(),
        Car.entry_time.desc()
    ).all()