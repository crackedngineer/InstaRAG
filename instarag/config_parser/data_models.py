from pydantic import BaseModel, Field
from typing import List, Optional


class CredentialModel(BaseModel):
    api_key: str


class ModelDetailsConfig(BaseModel):
    credentials: CredentialModel
    model_name: Optional[str] = None


class ModelConfig(BaseModel):
    chat: ModelDetailsConfig
    embeddings: ModelDetailsConfig
    image_generation: Optional[ModelDetailsConfig]


class Settings(BaseModel):
    logo: Optional[str] = ""
    readme: Optional[str] = ""
    theme: str = Field(default="system", pattern="^(light|dark|system)$")
    type: Optional[str] = None


class SourceConfig(BaseModel):
    type: str
    data: str


class AuthorConfig(BaseModel):
    name: str
    email: str


class ConfigSchema(BaseModel):
    name: str
    title: str
    description: str
    version: str
    authors: List[AuthorConfig]

    settings: Settings
    secrets: dict
    models: ModelConfig
    source: List[SourceConfig]
