from pydantic import BaseModel, Field
from pathlib import Path
from typing import List, Any, Optional
from src.core.nodes.document_loader.document_model import (
    SplitDocumentInput,
)
from src.core.common_models import UserProperties, DEFAULT_USER_ID, DEFAULT_SESSION_ID
from langchain.docstore.document import Document as LangchainDocument
from enum import Enum

DEFAULT_VECTORSTORE_FOLDER = Path("src/data/vectorstore/")


class SimilaritySearchInput(BaseModel):
    """
    Input model for similarity search.
    """

    query: str = Field(description="Input text for similarity search.")
    k: int = Field(4, description="Top k results for similarity search.")


class AddIndexInput(BaseModel):
    """
    Input model for adding an index.
    """

    user_properties: Optional[UserProperties] = Field(
        UserProperties(), description="User properties."
    )
    index_name: Optional[str] = Field(
        default="default", description="Name of the index."
    )
    split_documents: Optional[List[SplitDocumentInput]] = Field(
        default=[], description="List of split documents for creating the index."
    )
    connection: Any = Field(default="local", description="How to store the index.")


class DocumentIndexInfo(BaseModel):
    """
    Model for document index information.
    """

    user_properties: Optional[UserProperties] = Field(
        UserProperties(), description="User properties."
    )
    index_name: Optional[str] = Field(
        default="default", description="Name of the index."
    )
    index_id: Optional[str] = Field(default=None, description="ID of the index.")
    index_path: Optional[str] = Field(default=None, description="Path of the index.")
    index_pkl_path: Optional[str] = Field(
        default=None, description="Path of the index pickle file."
    )
    connection: Any = Field(default="local", description="How to store the index.")
    segmented_documents: Optional[List[LangchainDocument]] = Field(
        default=[], description="List of documents for creating the index."
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
