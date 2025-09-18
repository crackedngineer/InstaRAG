class ConfigReaderError(Exception):
    """Base exception for ConfigReader."""

    pass


class FileNotFoundError(ConfigReaderError):
    """Raised when the configuration file is not found."""

    def __init__(self, path: str):
        super().__init__(f"Configuration file not found: {path}")


class YAMLParseError(ConfigReaderError):
    """Raised when there is an error parsing the YAML file."""

    def __init__(self, error: str):
        super().__init__(f"Error parsing YAML file: {error}")


class SchemaValidationError(ConfigReaderError):
    """Raised when the configuration doesn't match the schema."""

    def __init__(self, errors: str):
        super().__init__(f"Schema validation failed:\n{errors}")


class SecretReplacementError(ConfigReaderError):
    """Raised when an error occurs during placeholder replacement."""

    def __init__(self, placeholder: str):
        super().__init__(f"Failed to replace placeholder: {placeholder}")
