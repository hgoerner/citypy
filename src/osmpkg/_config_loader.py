# This is a placeholder for correct code for this message.
import json


class ConfigLoader:

    @staticmethod
    def load_node_tags():
        node_tag_file = r"config\node_tags.json"
        try:
            with open(node_tag_file, "r", encoding="utf8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            return {}

    @staticmethod
    def load_relation_tags():
        relation_tag_file = r"config\relation_tags.json"
        try:
            with open(relation_tag_file, "r", encoding="utf8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            return {}

    # TODO, add function to change config file with city etc.
