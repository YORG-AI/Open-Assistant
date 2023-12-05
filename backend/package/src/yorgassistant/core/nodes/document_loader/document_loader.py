from fastapi import UploadFile, File, Form
from typing import Optional, Union
from pathlib import Path
from git import Repo

from langchain.document_loaders import CSVLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import GitLoader
from langchain.document_loaders import WebBaseLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

import json
import os
import shutil

from .document_model import Document, SplitDocumentInput, UrlDocumentInput
from ...common_models import (
    UserProperties,
    RedisKeyType,
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID,
    DEFAULT_GIT_FOLDER,
)
from ..base_node import BaseNode, NodeConfig
from ...service.redis import Redis
from ....utils.logger import get_logger


logger = get_logger(__name__)

document_loader_config = {
    "name": "document_loader",
    "description": "A node that is capable of reading various document types. Redis key format would be user_id:session_id:documents",
    "functions": {
        "create_document_from_file": "Create a document from a given file.",
        "create_document_from_url": "Create a document from a given URL.",
        "split_documents": "Split the documents from the file with default chunk size and overlap.",
        "process_document": "Process the file's content into text",
        "remove_document": "Remove the document from the Redis and local.",
    },
}


class DocumentLoaderNode(BaseNode):
    config: NodeConfig = NodeConfig(**document_loader_config)

    def __init__(self):
        super().__init__()
        self.redis = Redis()

    def create_document_from_file(
        self,
        input: UploadFile = File(...),
        properties: UserProperties = Form(...),
    ):
        document = Document.create_document_from_file(input, properties)
        return self.process_document(document)

    def create_document_from_url(
        self,
        input: UrlDocumentInput,
        properties: UserProperties = Form(...),
    ):
        document = Document.create_document_from_url(input, properties)
        return self.process_document(document)

    def split_documents(self, input: SplitDocumentInput):
        if input.file_id is None and input.document is None:
            logger.error("Either file_id or document must be provided.")
            return None
        elif input.file_id is not None:
            logger.debug(f"Spliting documents for: {input.file_id}")
            for doc_json in self.redis.safe_get_with_key_type(
                input.user_properties, RedisKeyType.DOCUMENTS
            ):
                doc = Document(**json.loads(doc_json))
                if doc.file_id == input.file_id:
                    return self._split_documents(
                        doc, input.chunk_size, input.chunk_overlap
                    )
            return None
        elif input.document is not None:
            return self._split_documents(
                input.document, input.chunk_size, input.chunk_overlap
            )
        else:
            raise ValueError("Unknown error")

    def process_document(self, input: Document):
        """
        Process the file to compute the documents

        Args:
            input (Document): The document to process
            save_redis (bool, optional): Whether to save the document to Redis. Defaults to True.
        """
        file_path = str(input.file_path)
        if input.file_extension == "csv":
            loader = CSVLoader(file_path)
        elif input.file_extension == "docx":
            loader = Docx2txtLoader(file_path)
        elif input.file_extension == "pdf":
            loader = PyMuPDFLoader(file_path)
        elif input.file_extension == "txt":
            loader = TextLoader(file_path)
        elif input.file_extension == "web":
            loader = WebBaseLoader(input.file_name)
        elif input.file_extension == "git":
            repo_path = input.file_path
            repo_path_str = str(repo_path) + "/"
            repo_path.parent.mkdir(parents=True, exist_ok=True)
            repo = Repo.clone_from(input.file_name, repo_path_str)
            branch = repo.head.reference
            gitignore_file = os.path.join(repo_path_str, ".gitignore")
            if os.path.exists(gitignore_file):
                os.remove(gitignore_file)
            with open(gitignore_file, "w") as fp:
                pass

            loader = GitLoader(repo_path=repo_path_str, branch=branch)
            # TODO: not sure why some repo gitignore would ignore all files
            # loader = GitLoader(
            #     clone_url=input.file_name,
            #     repo_path=str(repo_path) + "/",
            #     branch="main",
            #     file_filter=lambda file_path: file_path.endswith(".py")
            # )
        elif input.file_extension == "json":
            # TODO: JSONLoader needs to input json schema metadata
            # loader = TextLoader(
            #     file_path=input.file_path,
            # )
            pass
        else:
            raise ValueError(f"Unsupported file extension: {input.file_extension}")

        documents = loader.load()
        input.documents = documents
        if not self.redis.exists_with_key_type(
            input.user_properties, RedisKeyType.DOCUMENTS
        ):
            logger.debug(
                f"Creating new knowledge base for {input.user_properties.user_id}:{input.user_properties.session_id} in Redis."
            )
            self.redis.safe_set_with_key_type(
                input.user_properties, RedisKeyType.DOCUMENTS, []
            )

        new_documents = self.redis.safe_get_with_key_type(
            input.user_properties, RedisKeyType.DOCUMENTS
        )
        new_documents.append(input.json())

        self.redis.safe_set_with_key_type(
            input.user_properties, RedisKeyType.DOCUMENTS, new_documents
        )
        return input.json()

    def remove_document(self, input: Document):
        if input.file_path is not None:
            if os.path.isfile(input.file_path):
                os.remove(input.file_path)
            elif os.path.isdir(input.file_path):
                shutil.rmtree(input.file_path)  # remove dir and all contains

        type = RedisKeyType.DOCUMENTS
        if not self.redis.exists_with_key_type(input.user_properties, type):
            logger.error(f"Document {input.file_name} does not exist.")
            return

        all_documents = self.redis.safe_get_with_key_type(input.user_properties, type)
        processed_documents = []
        for doc_json in all_documents:
            doc = Document(**json.loads(doc_json))
            if doc.file_id != input.file_id:
                processed_documents.append(doc_json)

        self.redis.safe_set_with_key_type(
            input.user_properties, type, processed_documents
        )

    def _split_documents(
        self,
        input: Document,
        chunk_size: Optional[int] = 500,
        chunk_overlap: Optional[int] = 0,
    ):
        """
        Split the documents from the file
        """
        logger.debug(f"Spliting documents from file {input.file_name}")

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        documents = text_splitter.split_documents(input.documents)
        return documents
