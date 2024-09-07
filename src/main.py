from osmpkg._config_validator import ConfigValidator
from osmpkg._config_loader import ConfigLoader

# This block will only run if the script is executed directly
if __name__ == "__main__":
    # Initialize the class
    nodes = ConfigLoader.load_node_tags()
    areas = ConfigLoader.load_relation_tags()

    instance1 = ConfigValidator.validate_json_structure(nodes)
    instance2 = ConfigValidator.validate_json_structure(areas)

    # Call some method after initialization
