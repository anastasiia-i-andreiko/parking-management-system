from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal
import logic

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/park', methods=['POST'])
def park_car():
    data = request.json
    db = SessionLocal()
    try:
        car, error = logic.add_car(db, data.get('plate_number'), data.get('vehicle_type'))

        if error:
            return jsonify({"error": error}), 400

        # Зберігаємо ID в окрему змінну ПЕРЕД тим, як закрити сесію
        car_id = car.id
        db.commit()
        return jsonify({"message": "Авто додано", "id": car_id}), 201
    except Exception as e:
        print(f"Помилка: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route('/api/cars', methods=['GET'])
def get_cars():
    db = SessionLocal()
    search = request.args.get('search')
    # Викликаємо логіку отримання списку
    cars = logic.get_filtered_cars(db, search)

    result = []
    for c in cars:
        result.append({
            "id": c.id,
            "plate": c.plate_number,
            "type": c.vehicle_type,
            "status": c.status
        })
    db.close()
    return jsonify(result)


@app.route('/api/park/<int:car_id>', methods=['DELETE'])
def remove_car(car_id):
    db = SessionLocal()
    try:
        # Шукаємо машину за ID
        from models import Car
        car = db.query(Car).filter(Car.id == car_id).first()

        if not car:
            return jsonify({"error": "Машину не знайдено"}), 404

        db.delete(car)
        db.commit()
        return jsonify({"message": "Авто виїхало успішно"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/exit/<int:car_id>', methods=['PATCH'])
def exit_car(car_id):
    db = SessionLocal()
    success = logic.mark_exit(db, car_id)
    db.close()

    if success:
        return jsonify({"message": "Виїзд зафіксовано"}), 200
    return jsonify({"error": "Авто не знайдено або вже виїхало"}), 404


if __name__ == "__main__":
    from models import Base
    from database import engine

    # Base.metadata.drop_all(bind=engine)  <-- Закоментуй це (додай # попереду)
    Base.metadata.create_all(bind=engine)

    print("БАЗУ ПЕРЕЗАВАНТАЖЕНО ✅")
    app.run(debug=True)