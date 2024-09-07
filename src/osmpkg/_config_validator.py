class _ConfigValidator:
    @staticmethod
    def validate_config(config_data):
        """Validates configuration data for required fields."""
        if "category" not in config_data:
            raise ValueError("Config data missing required 'category' field")
        # Add more validation logic
        return True
