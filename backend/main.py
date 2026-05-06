from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal, engine
from models import Base, Car
import logic

app = Flask(__name__)
CORS(app)


@app.route('/api/park', methods=['POST'])
def park_car():
    data = request.json
    db = SessionLocal()
    try:
        car, error = logic.add_car(db, data.get('plate_number'), data.get('vehicle_type'))
        if error:
            return jsonify({"error": error}), 400

        db.commit()
        db.refresh(car)
        return jsonify({
            "message": "Авто додано успішно",
            "id": car.id,
            "status": car.status
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route('/api/cars', methods=['GET'])
def get_cars():
    db = SessionLocal()
    try:
        cars = logic.get_filtered_cars(db)
        result = []
        for c in cars:
            result.append({
                "id": c.id,
                "plate": c.plate_number,
                "type": c.vehicle_type,
                "status": c.status,
                "entry": c.entry_time.strftime('%H:%M') if c.entry_time else "--:--"
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route('/api/exit/<int:car_id>', methods=['PATCH'])
def exit_car(car_id):
    db = SessionLocal()
    try:
        success = logic.mark_exit(db, car_id)
        if success:
            db.commit()
            return jsonify({"message": "Виїзд зафіксовано"}), 200
        return jsonify({"error": "Авто не знайдено або вже виїхало"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("БАЗА ДАНИХ ГОТОВА ✅")
    app.run(debug=True, port=8000)