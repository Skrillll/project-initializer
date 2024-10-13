# Directory: project_initializer/
# File: config_loader.py

"""Module for loading configuration files for the project initializer."""

import yaml

class ConfigLoader:
    """A class for loading and parsing configuration files."""

    @staticmethod
    def load_config(config_path):
        """
        Load and parse a YAML configuration file.

        Args:
            config_path (str): The path to the YAML configuration file.

        Returns:
            dict: A dictionary containing the parsed configuration.

        Raises:
            FileNotFoundError: If the specified configuration file does not exist.
            yaml.YAMLError: If the configuration file is not valid YAML.
        """
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
