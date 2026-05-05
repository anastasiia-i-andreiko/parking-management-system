from datetime import datetime

class ParkingRecord:
    def __init__(self, plate, v_type):
        # Номер авто завжди ВЕЛИКИМИ літерами!!!
        self.plate = plate.upper()
        self.v_type = v_type             # "car" або "motorcycle"
        self.entry_time = datetime.now() # Час заїзду (автоматично)
        self.status = "parked"           # Статус на початку

    def to_dict(self):
        """Перетворення даних в словник для передачі на фронтенд"""
        return {
            "plate": self.plate,
            "v_type": self.v_type,
            "entry_time": self.entry_time.strftime("%H:%M:%S"),
            "status": self.status
        }