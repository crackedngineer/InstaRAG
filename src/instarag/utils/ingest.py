from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    WebBaseLoader,
)
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.generic import GenericLoader

# from langchain_community.document_loaders.parsers import OpenAIWhisperParser,OpenAIWhisperParserLocal
# from langchain.document_loaders.parsers.audio import (
#     OpenAIWhisperParser,
#     OpenAIWhisperParserLocal,
# )
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain_community.vectorstores import Qdrant

from .constants import ProcessorType
from .helpers import get_content_type

# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from streamlit import secrets, error, stop
# import psutil


class BaseSourceProcessor(ABC):
    @abstractmethod
    def load(self, **kwargs):
        pass

    def process(self, **kwargs):
        document = self.load(**kwargs)
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=1000,
            chunk_overlap=300,
            length_function=len,
        )
        chunks = text_splitter.split_documents(document)
        # chunks = text_splitter.create_documents(document)
        return chunks


class FileProcessor(BaseSourceProcessor):
    def __init__(self, fileLocation):
        self.fileLocation = Path(fileLocation).resolve()

    def load(self):
        contentType = get_content_type(self.fileLocation)
        # matching the file types for loaders
        if contentType == "text/plain":
            loader = TextLoader(self.fileLocation)
            document = loader.load()
        elif contentType == "application/pdf":
            loader = PyPDFLoader(self.fileLocation)
            document = loader.load_and_split()
        elif (
            contentType
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            loader = Docx2txtLoader(self.fileLocation)
            document = loader.load()
        elif (
            contentType
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            loader = UnstructuredExcelLoader(self.fileLocation)
            document = loader.load()
        elif contentType == "text/csv":
            loader = CSVLoader(self.fileLocation)
            document = loader.load()
        elif (
            contentType == "application/vnd.ms-powerpoint"
            or contentType
            == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ):
            loader = UnstructuredPowerPointLoader(self.fileLocation)
            document = loader.load()
        else:
            # for unsupported file type
            return []

        return document


class WebContentProcessor(BaseSourceProcessor):
    def __init__(self, url):
        self.url = url

    def process(self):
        loader = WebBaseLoader(self.url)
        data = loader.load()

        return data


class YouTubeChatProcessor(BaseSourceProcessor):
    def __init__(self, url, save_dir, local=False):
        self.url = url
        self.save_dir = save_dir
        self.local = local

    def load(self):
        if self.local:
            loader = GenericLoader(
                YoutubeAudioLoader([self.url], self.save_dir),
                # OpenAIWhisperParserLocal(),
            )
        else:
            loader = GenericLoader(
                YoutubeAudioLoader([self.url], self.save_dir), OpenAIWhisperParser()
            )
        docs = loader.load()
        return docs


def get_source_processor(type: str, source_data: str) -> BaseSourceProcessor:
    if type == ProcessorType.DOCUMENT.value:
        return FileProcessor(fileLocation=source_data)
    elif type == ProcessorType.WEB.value:
        return WebContentProcessor(url=source_data)
    elif type == ProcessorType.YOUTUBE.value:
        return YouTubeChatProcessor(url=source_data)
    raise ValueError("Invalid Source")