import mimetypes
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
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

# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from streamlit import secrets, error, stop
# import psutil

def get_content_type(filepath: str) -> str:
    """
    Determine the content type of the file using its extension and inspection.
    """
    # Determine MIME type by file name extension
    mimetype_by_name, _ = mimetypes.guess_type(filepath)

    # Fallback: Inspect the file's content (basic heuristic)
    def inspect_file_content(file_path: str) -> str:
        with open(file_path, "rb") as file:
            header = file.read(512)  # Read the first 512 bytes for inspection
        if b"%PDF-" in header:
            return "application/pdf"
        elif b"PK" in header and b"[Content_Types].xml" in header:
            return "application/vnd.openxmlformats-officedocument"
        elif b"<!DOCTYPE html>" in header or b"<html>" in header:
            return "text/html"
        elif b"," in header or b";" in header:
            return "text/csv"
        elif b"\t" in header:
            return "text/tsv"
        else:
            return "application/octet-stream"  # Default binary type

    # Return MIME type by name or inspect the file content as a fallback
    return mimetype_by_name or inspect_file_content(filepath)

class BaseSourceProcessor(ABC):
    @abstractmethod
    def load(self, **kwargs):
        pass

    def process(self, **kwargs):
        document = self.load(**kwargs)
        if document is None:
            return []
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
    def __init__(self, file_location):
        self.file_location = Path(file_location).resolve()

    def load(self):
        contentType = get_content_type(str(self.file_location))
        # matching the file types for loaders
        if contentType == "text/plain":
            loader = TextLoader(self.file_location)
            document = loader.load()
        elif contentType == "application/pdf":
            loader = PyPDFLoader(self.file_location)
            document = loader.load_and_split()
        elif (
            contentType
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            loader = Docx2txtLoader(self.file_location)
            document = loader.load()
        elif (
            contentType
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            loader = UnstructuredExcelLoader(self.file_location)
            document = loader.load()
        elif contentType == "text/csv":
            loader = CSVLoader(self.file_location)
            document = loader.load()
        elif (
            contentType == "application/vnd.ms-powerpoint"
            or contentType
            == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ):
            loader = UnstructuredPowerPointLoader(self.file_location)
            document = loader.load()
        else:
            # for unsupported file type
            return []

        return document


class WebContentProcessor(BaseSourceProcessor):
    def __init__(self, url):
        self.url = url

    def load(self):
        loader = WebBaseLoader(self.url)
        data = loader.load()

        return data


# class YouTubeChatProcessor(BaseSourceProcessor):
#     def __init__(self, url, save_dir, local=False):
#         self.url = url
#         self.save_dir = save_dir
#         self.local = local

#     def load(self):
#         if self.local:
#             loader = GenericLoader(
#                 YoutubeAudioLoader([self.url], self.save_dir),
#                 OpenAIWhisperParserLocal(),
#             )
#         else:
#             loader = GenericLoader(
#                 YoutubeAudioLoader([self.url], self.save_dir), OpenAIWhisperParser()
#             )
#         docs = loader.load()
#         return docs


def get_source_processor(type: str, data: dict) -> BaseSourceProcessor:
    if type == ProcessorType.DOCUMENT.value:
        file_location = data.get("path")
        return FileProcessor(file_location=file_location)
    elif type == ProcessorType.WEB.value:
        url = data.get("url")
        return WebContentProcessor(url=url)
    # elif type == ProcessorType.YOUTUBE.value:
    #     url = data.get("url")
    #     save_dir = data.get("save_dir", "./")
    #     local = data.get("local", False)
    #     return YouTubeChatProcessor(url=url, save_dir=save_dir, local=local)
    raise ValueError("Invalid Source")
