# overpass_query.py

# Private class for building queries
import urllib.parse
from _config_loader import ConfigLoader


class _OverpassQueryBuilder:
    def __init__(self):
        # Load separate config files for nodes and areas
        # TODOBuild config loader
        self.node_config = ConfigLoader.load_node_tags()
        self.area_config = ConfigLoader.load_relation_tags()

    def build_combined_query(
        self, country_code, city, admin_level_country, admin_level_city
    ):
        query_parts = []

        # Build node queries
        for osm_key, osm_value in self.node_config.items():
            encoded_key = urllib.parse.quote(osm_key)
            if osm_value is None:
                query_parts.append(f"node[{encoded_key}](area.city)(area.country);")
            else:
                encoded_value = urllib.parse.quote(osm_value)
                query_parts.append(
                    f"node[{encoded_key}={encoded_value}](area.city)(area.country);"
                )

        # Build area queries (ways/relations)
        for osm_key, osm_value in self.area_config.items():
            encoded_key = urllib.parse.quote(osm_key)
            if osm_value is None:
                query_parts.extend(
                    (
                        f"way[{encoded_key}](area.city)(area.country);",
                        f"relation[{encoded_key}](area.city)(area.country);",
                    )
                )
            else:
                encoded_value = urllib.parse.quote(osm_value)
                query_parts.extend(
                    (
                        f"way[{encoded_key}={encoded_value}](area.city)(area.country);",
                        f"relation[{encoded_key}={encoded_value}](area.city)(area.country);",
                    )
                )
        return f"""
        area["ISO3166-1"={country_code}][admin_level={admin_level_country}]->.country;
        area["name"="{city}"][admin_level={admin_level_city}]->.city;
        (
        {" ".join(query_parts)}
        );
        (._;>;);  /* Get the geometry for ways and relations */
        out geom;
        """
