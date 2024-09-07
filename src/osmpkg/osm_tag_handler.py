import json


class KeyValueDataValidator:
    @staticmethod
    def validate_json_structure(data):
        """Validate that the config data is a dictionary with valid key-value pairs."""
        if not isinstance(data, dict):
            print("Config is not a dictionary.")
            return False

        # Validate each key-value pair
        for key, value in data.items():
            if not isinstance(key, str):
                print(f"Key '{key}' is not a string.")
                return False
            if value is not None and not isinstance(value, str):
                print(f"Value for key '{key}' should be either a string or null.")
                return False

        print("Config is valid.")
        return True


class TagLoader:
    @staticmethod
    def load_osm_key_value(file_path):
        """Load the configuration file and validate its structure."""
        try:
            with open(file_path, "r") as file:
                config = json.load(file)  # First, load the JSON data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading config file: {e}")
            return None  # Return None if there's an issue loading the file

        # Now validate the loaded data
        return config if KeyValueDataValidator.validate_json_structure(config) else None

