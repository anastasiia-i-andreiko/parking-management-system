from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.database import SessionLocal, engine, Base
from backend.logic import get_stats, get_all_cars, add_car

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)


@app.route('/api/stats', methods=['GET'])
def stats_route():
    db = SessionLocal()
    try:
        stats = get_stats(db)
        return jsonify(stats)
    finally:
        db.close()


@app.route('/api/cars', methods=['GET'])
def cars_route():
    db = SessionLocal()
    try:
        cars = get_all_cars(db)
        return jsonify(cars)
    finally:
        db.close()


@app.route('/api/park', methods=['POST'])
def park_route():
    data = request.json
    plate = data.get('plate_number')

    db = SessionLocal()
    try:
        new_car, error = add_car(db, plate)
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"message": f"Car {plate} parked", "id": new_car.id}), 201
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)