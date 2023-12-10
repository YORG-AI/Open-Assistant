from pydantic import BaseModel, Field
from fastapi import UploadFile, File
from typing import List, Any, Optional
from langchain.docstore.document import Document as LangchainDocument
from pathlib import Path
from datetime import datetime
import hashlib

from ....utils.logger import get_logger
from ...common_models import (
    UserProperties,
    DEFAULT_DOCUMENTS_FOLDER,
    DEFAULT_GIT_FOLDER,
    TIME_STRING_FORMAT,
)


logger = get_logger(__name__)


class UrlDocumentInput(BaseModel):
    url: str = Field(description="Url for generating documents")
    type: str = Field(description="Type of loader used for this url")


class Document(BaseModel):
    user_properties: Optional[UserProperties] = Field(
        UserProperties(), description="User properties."
    )
    file_id: Optional[str] = Field(
        None,
        description="The ID of the uploaded file, generated using the user ID, session ID, and file name.",
    )
    file_path: Optional[Path] = Field(
        None, description="The path to the uploaded file."
    )
    file_name: Optional[str] = Field(
        None,
        description="The name of the uploaded file, including the timestamp of the upload.",
    )
    file_extension: Optional[str] = Field(
        "", description="The extension of the uploaded file."
    )
    file_size: Optional[int] = Field(
        None, description="The size of the uploaded file in bytes."
    )
    creation_time: Optional[str] = Field(
        None,
        description="The timestamp of the upload in the format 'YYYY-MM-DD-HH:MM:SS'.",
    )
    documents: Optional[List[LangchainDocument]] = Field(
        [],
        description="A list of LangchainDocument objects representing the uploaded file.",
    )

    def __init__(self, **kwargs):
        """
        Initializes a new Document object.

        Args:
            input (UploadFile): The uploaded file.
        """
        super().__init__(**kwargs)

    @classmethod
    def create_document_from_file(cls, input: UploadFile, properties: UserProperties):
        """
        Creates a new Document object from an UploadFile input.

        Args:
            input (UploadFile): The uploaded file.

        Returns:
            Document: A new Document object.
        """
        current_time = datetime.now().strftime(TIME_STRING_FORMAT)
        file_name = f"{current_time}-{input.filename}"
        file_path = (
            DEFAULT_DOCUMENTS_FOLDER
            / properties.user_id
            / properties.session_id
            / file_name
        )
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(input.file.read())

        file_id = hashlib.sha256(
            f"{properties.user_id}-{properties.session_id}-{file_name}".encode()
        ).hexdigest()
        file_extension = file_name.split(".")[-1].lower()
        file_size = input.file._file.tell()
        creation_time = current_time

        return cls(
            user_properties=UserProperties(**properties.dict()),
            file_id=file_id,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size,
            creation_time=creation_time,
        )

    @classmethod
    def create_document_from_url(
        cls, input: UrlDocumentInput, properties: UserProperties
    ):
        current_time = datetime.now().strftime(TIME_STRING_FORMAT)
        file_name = input.url
        file_id = hashlib.sha256(
            f"{properties.user_id}-{properties.session_id}-{file_name}".encode()
        ).hexdigest()
        file_path = None
        file_extension = input.type
        creation_time = current_time
        if input.type == "git":
            file_path = (
                DEFAULT_GIT_FOLDER
                / properties.user_id
                / properties.session_id
                / input.url.split("/")[-1]
            )
            file_path.parent.mkdir(parents=True, exist_ok=True)

        return cls(
            user_properties=UserProperties(**properties.dict()),
            file_id=file_id,
            file_name=file_name,
            file_path=file_path,
            file_extension=file_extension,
            creation_time=creation_time,
        )


class SplitDocumentInput(BaseModel):
    user_properties: Optional[UserProperties] = UserProperties()
    file_id: Optional[str] = None
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 0
    document: Optional[Document] = None
