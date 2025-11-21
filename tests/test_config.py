import unittest
import json  # you can use toml, json,yaml, or ryo for your config file
import sys,os
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)
sys.path.append(os.path.join(parent, "smartpark"))
from config_parser import parse_config

class TestConfigParsing(unittest.TestCase):
    def setUp(self):
        # TODO: read from a configuration file...
        self.test_filename = "test_config.json"
        self.test_data={
    "car_parks": [
        {
            "name": "raf-park-international",
            "total_spaces": 130,
            "total_cars": 0,
            "location": "moondalup",
            "broker": "localhost",
            "port": 1883,
            "sensors": [
                {
                    "name": "sensor1",
                    "type": "entry"
                },
                {
                    "name": "sensor2",
                    "type": "exit"
                }
            ],
            "displays": [
                {
                    "name": "display1"
                }
            ]
        }
    ]
}
        with open(self.test_filename, 'w') as f:
            json.dump(self.test_data, f)
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_parse_config(self):
        result = parse_config(self.test_filename)
        self.assertEqual(result["total_spaces"], 130)
        self.assertEqual(result["total_cars"], 0)

# TODO: create an additional TestCase in a separate file with at least one test of the remaining classes. 

if __name__=="__main__":
    unittest.main()