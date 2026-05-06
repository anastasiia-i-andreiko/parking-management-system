from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal
import logic

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
    result = [{
        "id": c.id,
        "plate": c.plate_number,
        "type": c.vehicle_type,
        "entry": c.entry_time.isoformat(),
        "status": c.status
    } for c in cars]
    db.close()
    return jsonify(result)


@app.route('/api/exit/<int:car_id>', methods=['PATCH'])
def exit_car(car_id):
    db = SessionLocal()
    success = logic.mark_exit(db, car_id)
    db.close()

    if success:
        return jsonify({"message": "Виїзд зафіксовано"}), 200
    return jsonify({"error": "Авто не знайдено або вже виїхало"}), 404


if __name__ == "__main__":
    app.run(debug=True)