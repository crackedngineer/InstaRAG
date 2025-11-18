import os
from langchain_core.vectorstores import VectorStore, InMemoryVectorStore
from langchain_chroma import Chroma
from instarag.core.enum import VectorStoreType
from .constants import VECTOR_STORE_DEFAULT_PARAMS


def get_vector_store(store_type: str = "inmemory", **kwargs) -> VectorStore:
    if store_type == VectorStoreType.INMEMORY.value:
        return InMemoryVectorStore(**kwargs)
    elif store_type == VectorStoreType.CHROMA.value:
        return Chroma(
            collection_name=kwargs.get("collection_name", "default_collection"),
            embedding_function=kwargs.get("embedding_function"),
            persist_directory=kwargs.get(
                "persist_directory",
                f"{os.path.join(VECTOR_STORE_DEFAULT_PARAMS['persist_directory'], VectorStoreType.CHROMA.value)}",
            ),
        )
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")
