import yaml
from typing import Any, Optional
from pathlib import Path
from pydantic import ValidationError
from .schema import ConfigSchema
from .error import YAMLParseError, SchemaValidationError, SecretReplacementError


class ConfigParser:
    def __init__(self, file_path: str):
        """
        Initializes ConfigReader with the file path.
        """
        self.file_path = file_path
        self.__config: Optional[ConfigSchema] = None

    @property
    def file_path(self) -> Path:
        return self._file_path

    @file_path.setter
    def file_path(self, value: str | Path) -> None:
        """
        Sets the file path for the configuration file.
        If value is empty or invalid, attempts to use default config files.
        """
        if not value or str(value).strip() == "":
            candidates = [Path("instarag.config.yaml"), Path("instarag.config.yml")]
            for candidate in candidates:
                if candidate.is_file():
                    self._file_path = candidate
                    return
            raise ValueError("A valid configuration file path must be provided.")
        self._file_path = Path(value)

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

            # Validate against schema
            self.__config = ConfigSchema(**raw_data)

        except FileNotFoundError as e:
            raise FileNotFoundError(resolved_path) from e
        except yaml.YAMLError as e:
            raise YAMLParseError(str(e)) from e
        except ValidationError as e:
            raise SchemaValidationError(e)

    def get_value(self, key: str, default=None) -> Any:
        """
        Fetches a specific configuration value using dot notation.
        """
        keys = key.split(".")
        if self.__config is None:
            return default
        value = self.__config.model_dump()
        try:
            for k in keys:
                value = value[k]
        except (KeyError, TypeError):
            return default
        return value

    def get_config(self):
        return self.__config
