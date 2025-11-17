from ..core.enum import BaseEnum


class ModesEnum(BaseEnum):
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    IMAGE_GENERATION = "image_generation"
    VECTOR_STORE = "vector_store"


class ProcessorType(BaseEnum):
    WEB = "web"
    DOCUMENT = "document"
    YOUTUBE = "youtube"