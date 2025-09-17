from pathlib import Path
from config_parser import ConfigParser
from config_parser.error import ConfigReaderError


def parse_config(config_path: Path):
    try:
        config_parser = ConfigParser(config_path)
        config_parser.read_config()
        return config_parser.get_config()
    except ConfigReaderError as e:
        print(f"Configuration Error: {e}")


def load_source(details: list) -> list:
    chunk = list()
    for details in details:
        processor = get_source_processor(details.type, details.data)
        chunk.extend(processor.process())
    return chunk


def setup_vector_store():
    pass


def setup_embedding():
    pass


def store_embedding(embedding, vector_store, chunks):
    """
    Multiple PDF store and retrival technique
    Reference :- https://colab.research.google.com/drive/1gyGZn_LZNrYXYXa-pltFExbptIe7DAPe?usp=sharing
    """
    pass


def setup_model(model_detail: dict, embedded_obj):
    return Chat(
        model_name=model_detail.model_name, api_key=model_detail.credentials.api_key
    )
