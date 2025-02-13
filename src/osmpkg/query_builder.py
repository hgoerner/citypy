import json
import urllib.parse


class QueryBuilder:

    def __init__(self, node_file=r"config\node_tags.json", area_file=r"config\relation_tags.json"):
        """Initialize with file paths for the node and area configurations."""
        self.node_file = node_file
        self.area_file = area_file
        self.node_config = None
        self.area_config = None
        # Load and validate configurations
        self._load_and_validate()

    def _load_and_validate(self):
        """Load and validate both node and area configurations."""
        # Load node configuration
        self.node_config = self._load_file(self.node_file)
        if not self.node_config:
            print(f"Warning: Failed to load or validate node configuration from {self.node_file}. Continuing with area configuration.")

        # Load area configuration
        self.area_config = self._load_file(self.area_file)
        if not self.area_config:
            print(f"Warning: Failed to load or validate area configuration from {self.area_file}. Continuing with node configuration.")

    @staticmethod
    def _load_file(file_path):
        """Load and validate JSON data from a file."""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if QueryBuilder._validate_json_structure(data):
                    return data
                print(f"Validation failed for file: {file_path}")
                return None
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading file {file_path}: {e}")
            return None

    @staticmethod
    def _validate_json_structure(data):
        """Validate JSON structure to ensure it's a non-empty dictionary."""
        if not isinstance(data, dict) or not data:
            print("Data is not a valid non-empty dictionary.")
            return False

        for key, value in data.items():
            if not isinstance(key, str) or not key.strip():
                print(f"Invalid key '{key}', key must be a non-empty string.")
                return False
            if value is not None and not isinstance(value, str):
                print(f"Invalid value for key '{key}', value must be a string or None.")
                return False

        return True

    def build_single_queries(self, country_code, city, admin_level_country, admin_level_city):
        """Generate individual queries for the node and area configurations."""
        query_parts = []

        # Build node queries if valid node configuration exists
        if self.node_config:
            query_parts.extend(
                self._build_query_part(
                    osm_key,
                    osm_value,
                    "node",
                    country_code,
                    city,
                    admin_level_country,
                    admin_level_city,
                )
                for osm_key, osm_value in self.node_config.items()
            )

        # Build area queries if valid area configuration exists
        if self.area_config:
            for osm_key, osm_value in self.area_config.items():
                query_parts.append(
                    self._build_query_part(
                        osm_key,
                        osm_value,
                        "way",
                        country_code,
                        city,
                        admin_level_country,
                        admin_level_city,
                    )
                )
                query_parts.append(
                    self._build_query_part(
                        osm_key,
                        osm_value,
                        "relation",
                        country_code,
                        city,
                        admin_level_country,
                        admin_level_city,
                    )
                )

        # Return a list of single queries
        return query_parts

    @staticmethod
    def _build_query_part(osm_key, osm_value, element_type, country_code, city, admin_level_country, admin_level_city):
        encoded_key = urllib.parse.quote(osm_key)
        encoded_value = urllib.parse.quote(osm_value) if osm_value else None

        if element_type == "area":
            # Building query for both way and relation when the type is "area"
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            (
            way[{encoded_key}={encoded_value}](area.city)(area.country);
            relation[{encoded_key}={encoded_value}](area.city)(area.country);
            );
            (._;>;);
            out geom;
            """
        else:
            # Building query for individual elements like nodes
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            {element_type}[{encoded_key}={encoded_value}](area.city)(area.country);
            (._;>;);
            out geom;
            """
