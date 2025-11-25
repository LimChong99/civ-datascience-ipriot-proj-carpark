import unittest
import sys,os
from pathlib import Path

cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)
sys.path.append(os.path.join(parent, "smartpark"))

sys.path.append(parent + "/smartpark")

#Change the line below to import your manager class
from carpark import CarparkManager


class TestCarparkAlgorithms(unittest.TestCase):

    def setUp(self):
        self.carpark = CarparkManager()
        self.carpark.total_spaces = 5
        self.carpark.cars = []

    def test_initial_spaces(self):
        """Test 1: Checks if the carpark starts with correct available spaces."""
        self.assertEqual(self.carpark.available_spaces, 5)

    def test_entry_decrements_spaces(self):
        """Test 2: When a car enters, available spaces should go down."""
        self.carpark.incoming_car("ABC-123")
        self.assertEqual(self.carpark.available_spaces, 4)

    def test_exit_increments_spaces(self):
        """Test 3: When a car leaves, available spaces should go up."""
        self.carpark.incoming_car("ABC-123")
        self.carpark.outgoing_car("ABC-123")
        self.assertEqual(self.carpark.available_spaces, 5)

    def test_no_negative_spaces(self):
        """Test 4: Ensure we cannot fill the carpark beyond capacity."""
        for i in range(5):
            self.carpark.incoming_car(f"CAR-{i}")

        self.assertEqual(self.carpark.available_spaces, 0)
        self.carpark.incoming_car("CAR-OVERFLOW")
        self.assertEqual(self.carpark.available_spaces, 0)


if __name__ == "__main__":
    unittest.main()