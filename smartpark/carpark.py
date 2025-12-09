from pathlib import Path
from datetime import datetime
from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
from car import Car

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here.
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class CarparkManager(CarparkSensorListener, CarparkDataProvider):
    def __init__(self):
        self.total_spaces = 0
        self.cars = []
        self.current_temp = 25
        self.config_file = Path(__file__).parent.parent / "samples_and_snippets" / "config.json"
        self._load_config()
        self._log("Carpark Manager Initialized")
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)
        observer.update_display()

    def _publish_update(self):
        for observer in self.observers:
            observer.update_display()

    def _load_config(self):
        print(f"Loading config from: {self.config_file}")
        try:
            config_data = parse_config(str(self.config_file))
            self.total_spaces = int(config_data.get('total_spaces', 10))
            print(f"Config loaded. Total spaces: {self.total_spaces}")
        except Exception as e:
            print(f"Error loading config: {e}. Using default of 10 spaces.")
            self.total_spaces = 10

    def _log(self, message):
        log_file = Path(__file__).parent.parent / "carpark_log.txt"
        with open(log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")

    @property
    def available_spaces(self):
        """Requirement: The number of bays available"""
        # Logic: Total capacity minus the number of cars currently in the list
        return self.total_spaces - len(self.cars)

    @property
    def temperature(self):
        """Requirement: The current temperature"""
        return self.current_temp

    @property
    def current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def incoming_car(self, license_plate):
        if self.available_spaces <= 0:
            print(f"Entry denied for {license_plate}: Carpark Full")
            self._log(f"ENTRY DENIED (FULL): {license_plate}")
            return

        new_car = Car(license_plate)
        self.cars.append(new_car)

        print(f"Car in! {license_plate}")
        self._log(f"ENTERED: {license_plate}")
        self._publish_update()

    def outgoing_car(self, license_plate):
        found_car = None
        for car in self.cars:
            if car.license_plate == license_plate:
                found_car = car
                break

        if found_car:
            self.cars.remove(found_car)
            print(f"Car out! {license_plate}")
            self._log(f"EXITED: {license_plate}")
        else:
            print(f"Ghost car detected: {license_plate} tried to exit but was not found.")
            self._log(f"GHOST EXIT ATTEMPT: {license_plate}")
        self._publish_update()

    def temperature_reading(self, reading):
        self.current_temp = reading
        self._publish_update()