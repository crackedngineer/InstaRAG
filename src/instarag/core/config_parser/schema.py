import os
from pydantic import BaseModel, Field
from typing import List, Optional

from instarag.core.constants import THEMES_LIST

class EnvStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if isinstance(v, str) and v.startswith("$"):
            env_var = v[1:]
            env_value = os.getenv(env_var)
            if env_value is None:
                raise ValueError(f"Environment variable '{env_var}' not found")
            return env_value
        return v


class AuthorModel(BaseModel):
    name: str = Field(..., description="Author's name")
    email: str = Field(
        ...,
        description="Author's email",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )


class AuthorConfig():
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field) -> List[AuthorModel]:
        if isinstance(v, list):
            return [AuthorModel(**item) for item in v]
        res = []
        if isinstance(v, str):
            authors_list = [a.strip() for a in v.split(",")]
            if len(authors_list) == 0:
                raise ValueError("No authors found in the string.")
            for author_str in authors_list:
                if "<" in author_str and ">" in author_str:
                    name_part, email_part = author_str.split("<", 1)
                    name = name_part.strip()
                    email = email_part.strip(">").strip()
                    res.append(AuthorModel(name=name, email=email))
        return res


class CredentialModel(BaseModel):
    api_key: EnvStr = Field(..., description="API key for the model")


class ModelDetailsConfig(BaseModel):
    credentials: CredentialModel = Field(..., description="Credentials for the model")
    model_name: Optional[str] = Field(None, description="Name of the model")



class SourceConfig(BaseModel):
    type: str = Field(..., description="Type of the source, e.g., 'pdf', 'web', 'text'")
    params: List[str] = Field(
        ..., description="Data related to the source, e.g., file path or URL"
    )
    
class VectorStoreConfig(BaseModel):
    type: str = Field(..., description="Type of the vector store, e.g., 'inmemory', 'chroma'")
    params: Optional[dict] = Field(default_factory=dict, description="Parameters for the vector store")

class ConfigSchema(BaseModel):
    name: str = Field(..., description="Name of the application")
    title: str = Field(..., description="Title of the application")
    description: str = Field(..., description="Description of the application")
    version: str = Field(..., description="Version of the application")
    authors: AuthorConfig = Field(..., description="List of authors")
    tags: List[str] = Field(..., description="List of tags")
    logo: Optional[str] = Field(default="", description="Logo of the application")
    readme: Optional[str] = Field(default="", description="Readme file of the application")
    theme: str = Field(default="system", pattern=f"^({'|'.join(THEMES_LIST)})$", description="Theme of the application")
    sources: List[SourceConfig] = Field(..., description="List of source configurations")
    
    vector_store: VectorStoreConfig = Field(..., description="Vector store configuration")
    chat_model: ModelDetailsConfig = Field(..., description="Chat model configuration")
    embedding_model: ModelDetailsConfig = Field(..., description="Embeddings model configuration")
    image_generation_model: Optional[ModelDetailsConfig] = Field(None, description="Image generation model configuration")