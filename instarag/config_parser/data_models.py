from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

class ModelDetailsConfig(BaseModel):
    credentials: dict
    model_name: Optional[str] = None

class ModelConfig(BaseModel):
    chat: ModelDetailsConfig
    embeddings: ModelDetailsConfig
    image_generation: Optional[ModelDetailsConfig]


class Settings(BaseModel):
    logo: Optional[str] = ""
    readme: Optional[str] = ""
    theme: str = Field(default="system", pattern="^(light|dark|system)$")


class Meta(BaseModel):
    title: str

class SourceConfig(BaseModel):
    type: str
    data: str

class AuthorConfig(BaseModel):
    name: str
    email: str

class ConfigSchema(BaseModel):
    name: str
    description: str
    version: str
    authors: List[AuthorConfig]

    meta: Meta
    settings: Settings
    secrets: dict
    models: ModelConfig
    source: List[SourceConfig]
