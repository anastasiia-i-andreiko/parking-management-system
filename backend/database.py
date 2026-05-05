import json
import os

# Файл, де зберігаються дані
DB_PATH = os.path.join(os.path.dirname(__file__), "parking_data.json")

def load_data():
    """Завантажує список машин із JSON файлу"""
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, Exception):
        return []

def save_data(data):
    """Зберігає список машин у JSON файл"""
    try:
        with open(DB_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Помилка при збереженні: {e}")
        return False