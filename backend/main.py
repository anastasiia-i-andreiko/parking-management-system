from flask import Flask, jsonify, request
from flask_cors import CORS
from database import load_data, save_data
from logic import validate_plate, get_stats

app = Flask(__name__)
CORS(app)

@app.route('/api/stats', methods=['GET'])
def stats():
    """Повертає статистику парковки для фронтенду"""
    data = load_data()
    return jsonify(get_stats(data))

@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Повертає список усіх машин у форматі JSON"""
    return jsonify(load_data())

@app.route('/api/park', methods=['POST'])
def park_car():
    """Додає нове авто: отримує номер та тип від фронтенда"""
    req = request.json
    plate = req.get('plate', '').upper()
    v_type = req.get('v_type', 'car')

    if not validate_plate(plate):
        return jsonify({"error": "Невірний формат номера"}), 400

    data = load_data()
    new_record = {"plate": plate, "v_type": v_type, "status": "parked"}
    data.append(new_record)
    save_data(data)
    return jsonify({"message": "Авто додано", "car": new_record}), 201

if __name__ == '__main__':
    print("Сервер працює на http://127.0.0.1:5000")
    app.run(debug=True, port=5000)