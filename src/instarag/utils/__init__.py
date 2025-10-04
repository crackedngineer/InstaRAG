from pathlib import Path
from typing import List
from instarag.config_parser.data_models import SourceConfig

from ..config_parser import ConfigParser
from ..config_parser.error import ConfigReaderError
from .ingest import get_source_processor

def parse_config(config_path: Path):
    try:
        config_parser = ConfigParser(config_path)
        config_parser.read_config()
        return config_parser.get_config()
    except ConfigReaderError as e:
        print(f"Configuration Error: {e}")


def load_source(details: List[SourceConfig]) -> list:
    chunk = list()
    for detail in details:
        processor = get_source_processor(detail.type, detail.data)
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


# def setup_model(model_detail: dict, embedded_obj):
#     return Chat(
#         model_name=model_detail.model_name, api_key=model_detail.credentials.api_key
#     )
