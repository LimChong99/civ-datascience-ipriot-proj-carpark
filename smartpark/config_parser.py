"""A class or function to parse the config file and return the values as a dictionary.

The config file itself can be any of the following formats (recommend one of pandas, json, or ryo):

- You can use pandas to read a data file if you like. Something simple like a CSV would be best.

- ryo: means 'roll your own' and is a simple text file with key-value pairs separated by an equals sign. For example:
```
location = "Moondalup City Square Parking"
number_of_spaces = 192
```
**you** read the file and parse it into a dictionary.
- json: a json file with key-value pairs. For example:
```json
{location: "Moondalup City Square Parking", number_of_spaces: 192}
```
json is built in to python, so you can use the json module to parse it into a dictionary.
- toml: a toml file with key-value pairs. For example:
```toml
[location]
name = "Moondalup City Square Parking"
spaces = 192
```
toml is part of the standard library in python 3.11, otherwise you need to install tomli to parse it into a dictionary.
```bash
python -m pip install tomli
```
see [realpython.com](https://realpython.com/python-toml/) for more info.

Finally, you can use `yaml` if you prefer.



"""
import json
from pathlib import Path


def parse_config(config_file: str = "config.json") -> dict:
    """Parse the config file and return the values as a dictionary"""
    try:
        file_path = Path(config_file)
        with open(file_path, 'r') as input_file:
            config = json.load(input_file)
        if "car_parks" in config:
            return config["car_parks"][0]
        else:
            return config
    except FileNotFoundError:
        print("Config file not found")
        return {}
    except Exception as e:
       print(f"An error occurred: {e}")
       return {}


if __name__ == '__main__':
    current_dir = Path(__file__).parent
    config_path = current_dir.parent / "samples_and_snippets" / "config.json"
    print(f"Reading from: {config_path}")
    cfg_data = parse_config(str(config_path))
    print(cfg_data)
