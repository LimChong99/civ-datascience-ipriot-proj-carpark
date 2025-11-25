from datetime import datetime

class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate
        self.entry_time = datetime.now()

    def __str__(self):
        return f"Car: {self.license_plate}"

    @property
    def time_parked(self):
        return datetime.now() - self.entry_time