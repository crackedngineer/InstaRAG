from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def has_value(cls, value):
        return any(value == item.name for item in cls)

    @classmethod
    def fetch(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid value for {cls.__name__}")
    
class ModesEnum(BaseEnum):
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    IMAGE_GENERATION = "image_generation"
    VECTOR_STORE = "vector_store"


class ProcessorType(BaseEnum):
    WEB = "web"
    FILE = "file"

class VectorStoreType(BaseEnum):
    INMEMORY = "inmemory"
    CHROMA = "chroma"
    FAISS = "faiss"
    
class EmbeddingModelType(BaseEnum):
    OPENAI = "openai"
    GOOGLE_GENAI = "google_genai"
    HUGGINGFACE = "huggingface"