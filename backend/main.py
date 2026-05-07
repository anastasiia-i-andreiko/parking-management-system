from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal, engine
import models
import logic

# Автоматичне створення таблиць у базі даних (якщо їх ще немає)
models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)


@app.route('/api/park', methods=['POST'])
def park_car():
    data = request.json
    db = SessionLocal()
    car, error = logic.add_car(db, data.get('plate_number'), data.get('vehicle_type'))
    db.close()

    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Авто додано", "id": car.id}), 201


@app.route('/api/cars', methods=['GET'])
def get_cars():
    search = request.args.get('search')
    db = SessionLocal()
    cars = logic.get_filtered_cars(db, search)
    
    # Форматуємо дату прямо тут, щоб фронтенд отримав красивий текст
    result = [{
        "id": c.id,
        "plate": c.plate_number,
        "type": c.vehicle_type,
        "entry": c.entry_time.strftime("%d.%m.%Y %H:%M") if c.entry_time else '--:--',
        "status": c.status
    } for c in cars]
    
    db.close()
    return jsonify(result)


# Змінено шлях та метод під те, що очікує app.js (DELETE /api/park/<id>)
@app.route('/api/park/<int:car_id>', methods=['DELETE'])
def exit_car(car_id):
    db = SessionLocal()
    success = logic.mark_exit(db, car_id)
    db.close()

    if success:
        return jsonify({"message": "Виїзд зафіксовано"}), 200
    return jsonify({"error": "Авто не знайдено або вже виїхало"}), 404


if name == "__main__":
    app.run(debug=True)
