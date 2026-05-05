import re
from datetime import datetime

def validate_plate(plate):
    """Пункт 1а: Перевірка правильності номера автомобіля"""
    # Номер має бути від 4 до 10 символів (літери та цифри)
    return bool(re.match(r"^[A-Z0-9А-Я]{4,10}$", plate.upper()))

def find_car_by_plate(data, plate):
    """Пункт 4: Пошук автомобіля по номеру"""
    search_query = plate.upper()
    return [car for car in data if search_query in car['plate']]

def sort_by_entry_time(data):
    """Пункт 6: Сортувати записи по часу заїзду (від нових до старих)"""
    return sorted(data, key=lambda x: x['entry_time'], reverse=True)

def get_stats(data):
    """Пункт 7: Статистика (загальна кількість та на парковці)"""
    total = len(data)
    currently_parked = len([c for c in data if c['status'] == 'parked'])
    return {
        "total_visits": total,
        "on_parking": currently_parked
    }

def calculate_cost(entry_time_str, v_type):
    """Логіка для пункту 3: Оплата при виїзді"""
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        entry_time = datetime.strptime(entry_time_str, fmt)
        duration = datetime.now() - entry_time
        # Мінімум 1 година оплати
        hours = max(1, int(duration.total_seconds() // 3600))
        rate = 20 if v_type == 'car' else 10
        return hours * rate
    except:
        return 20 # Дефолтна ціна, якщо час збився