# src\src\osmpkg\_query_builder.py
# Private class for building queries
import urllib.parse
from osm_tag_handler import TagLoader


class _OverpassQueryBuilder:
    # Class-level variables to hold the configuration
    node_config = None
    area_config = None

    def __init__(self):
        # Load the configuration only if it hasn't been loaded yet
        if _OverpassQueryBuilder.node_config is None:
            _OverpassQueryBuilder.node_config = TagLoader.load_osm_key_value(r"config\node_tags.json")
            if _OverpassQueryBuilder.node_config is None:
                raise ValueError("Failed to load node configuration. Please check the file path or file content.")

        if _OverpassQueryBuilder.area_config is None:
            _OverpassQueryBuilder.area_config = TagLoader.load_osm_key_value(r"config\relation_tags.json")
            if _OverpassQueryBuilder.area_config is None:
                raise ValueError("Failed to load area configuration. Please check the file path or file content.")

    def _build_node_query(self, osm_key, osm_value, country_code, city, admin_level_country, admin_level_city):
        """Builds a single query for a node key-value pair."""
        encoded_key = urllib.parse.quote(osm_key)
        if osm_value is None:
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            node[{encoded_key}](area.city)(area.country);
            (._;>;);
            out geom;
            """
        else:
            encoded_value = urllib.parse.quote(osm_value)
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            node[{encoded_key}={encoded_value}](area.city)(area.country);
            (._;>;);
            out geom;
            """

    def _build_area_query(self, osm_key, osm_value, country_code, city, admin_level_country, admin_level_city):
        """Builds a single query for an area key-value pair (ways and relations)."""
        encoded_key = urllib.parse.quote(osm_key)
        if osm_value is None:
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            way[{encoded_key}](area.city)(area.country);
            relation[{encoded_key}](area.city)(area.country);
            (._;>;);
            out geom;
            """
        else:
            encoded_value = urllib.parse.quote(osm_value)
            return f"""
            area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
            area["name"="{city}"][admin_level={admin_level_city}]->.city;
            way[{encoded_key}={encoded_value}](area.city)(area.country);
            relation[{encoded_key}={encoded_value}](area.city)(area.country);
            (._;>;);
            out geom;
            """

    def build_single_queries(self, country_code, city, admin_level_country, admin_level_city):
        """Generates individual queries for both nodes and areas."""
        queries = []

        # Generate queries for node configuration
        for osm_key, osm_value in _OverpassQueryBuilder.node_config.items():
            query = self._build_node_query(
                osm_key, osm_value, country_code, city, admin_level_country, admin_level_city
            )
            queries.append(query)

        # Generate queries for area configuration (ways and relations)
        for osm_key, osm_value in _OverpassQueryBuilder.area_config.items():
            query = self._build_area_query(
                osm_key, osm_value, country_code, city, admin_level_country, admin_level_city
            )
            queries.append(query)

        return queries  # Return a list of individual queries
