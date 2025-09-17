import yaml
from typing import Any, Optional
from pathlib import Path
from pydantic import ValidationError
from config_parser.data_models import ConfigSchema
from config_parser.error import YAMLParseError, SchemaValidationError, SecretReplacementError


class ConfigParser:
    def __init__(self, file_path: Path):
        """
        Initializes ConfigReader with the file path.
        """
        self.file_path = file_path
        self.__config: Optional[ConfigSchema] = None

    def read_config(self) -> None:
        """
        Reads, validates, and parses the YAML configuration file.
        """
        try:
            # Resolve and read the YAML file
            resolved_path = Path(self.file_path).resolve()
            if not resolved_path.is_file():
                raise FileNotFoundError(resolved_path)

            with open(resolved_path, "r") as file:
                raw_data = yaml.safe_load(file)

            # Handle secrets
            self._handle_secrets(raw_data)

            # Validate against schema
            self.__config = ConfigSchema(**raw_data)

        except FileNotFoundError as e:
            raise FileNotFoundError(resolved_path) from e
        except yaml.YAMLError as e:
            raise YAMLParseError(str(e)) from e
        except ValidationError as e:
            raise SchemaValidationError(e.json()) from e

    def _handle_secrets(self, config: dict) -> None:
        """
        Replace placeholders in the configuration with secrets from the 'secrets' section.
        """
        secrets = config.get("secrets", {})
        for key, value in secrets.items():
            placeholder = f"${key}"
            try:
                self._replace_placeholders(config, placeholder, value)
            except Exception as e:
                raise SecretReplacementError(placeholder) from e

    @staticmethod
    def _replace_placeholders(data: Any, placeholder: str, value: str) -> None:
        """
        Recursively replaces placeholders in the configuration with actual secret values.
        """
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    ConfigParser._replace_placeholders(v, placeholder, value)
                elif isinstance(v, str) and placeholder in v:
                    data[k] = v.replace(placeholder, value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    ConfigParser._replace_placeholders(item, placeholder, value)
                elif isinstance(item, str) and placeholder in item:
                    data[i] = item.replace(placeholder, value)



    def get_value(self, key: str, default=None) -> Any:
        """
        Fetches a specific configuration value using dot notation.
        """
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
        except (KeyError, TypeError):
            return default
        return value
    
    def get_config(self):
        return self.__config
