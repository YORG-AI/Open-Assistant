from typing import List
from abc import ABC, abstractmethod
from pathlib import Path
import hashlib
import json
import os

from .vectorstore_model import (
    DocumentIndexInfo,
    SimilaritySearchInput,
    AddIndexInput,
    DEFAULT_VECTORSTORE_FOLDER,
)
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.document_loader.document_model import SplitDocumentInput
from src.core.nodes.document_loader.document_loader import DocumentLoaderNode
from src.core.common_models import RedisKeyType
from src.service.redis import Redis
from src.utils.logger import get_logger
from src.utils.router_generator import generate_node_end_points

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

logger = get_logger(__name__)


def get_vectorstore_config(name: str):
    return {
        "name": name,
        "description": "A node for managing and querying embeddings using VectorStore. Redis key format would be user_id:session_id:name",
        "functions": {
            "load_index": "Load an index from a given document index info.",
            "add_index": "Create an index from a given list of documents.",
            "save_index": "Save the created index and store its information in Redis.",
            "similarity_search": "Perform similarity search on the indexed embeddings.",
        },
    }


class VectorStoreNode(BaseNode, ABC):
    config: NodeConfig = NodeConfig(**get_vectorstore_config("vectorstore"))

    @abstractmethod
    def load_index(self, DocumentIndexInfo):
        raise NotImplementedError

    @abstractmethod
    def add_index(self, input):
        raise NotImplementedError

    @abstractmethod
    def save_index(self, input):
        raise NotImplementedError

    @abstractmethod
    def similarity_search(self, input):
        raise NotImplementedError

    @abstractmethod
    def remove_index(self, input):
        raise NotImplementedError


@generate_node_end_points
class FaissVectorStoreNode(VectorStoreNode):
    config: NodeConfig = NodeConfig(**get_vectorstore_config("faiss_vectorstore"))

    def __init__(self):
        super().__init__()
        self.redis = Redis()
        self.index = None
        self.documenn_index_info = None
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_EMBEDDINGS_API_KEY")
        )

    def load_index(self, input: DocumentIndexInfo):
        if input.index_path is None or input.index_pkl_path is None:
            logger.error("Both index_path and index_pkl_path must be provided.")
            return None
        folder_path = Path(input.index_path).parent
        self.index = FAISS.load_local(
            folder_path=str(folder_path),
            index_name=input.index_id,
            embeddings=self.embeddings,
        )
        self.documenn_index_info = input

    def add_index(self, input: AddIndexInput):
        segmented_documents = []
        for doc in input.split_documents:
            segmented_chunks = DocumentLoaderNode().split_documents(input=doc)
            segmented_documents += segmented_chunks

        if self.documenn_index_info is None:
            # there is no existing index and so it needs to create a new index
            self.index = FAISS.from_documents(
                segmented_documents,
                self.embeddings,
            )
            self.document_index_info = DocumentIndexInfo(
                user_properties=input.user_properties,
                index_name=input.index_name,
                index_id=hashlib.sha256(
                    f"{input.user_properties.user_id}-{input.user_properties.session_id}-{input.index_name}".encode()
                ).hexdigest(),
                segmented_documents=segmented_documents,
            )
        else:
            # append more documents to the existing index
            self.index = FAISS.from_documents(
                self.documenn_index_info.segmented_documents + segmented_documents,
                self.embeddings,
            )
            self.document_index_info.segmented_documents += segmented_documents

        if isinstance(input.connection, str):
            if input.connection == "local":
                return self.save_index(self.document_index_info)

    def save_index(self, input: DocumentIndexInfo):
        folder_path = (
            DEFAULT_VECTORSTORE_FOLDER
            / input.user_properties.user_id
            / input.user_properties.session_id
        )
        self.index.save_local(
            folder_path=str(folder_path),
            index_name=input.index_id,
        )
        input.index_path = str(folder_path / f"{input.index_id}.faiss")
        input.index_pkl_path = str(folder_path / f"{input.index_id}.pkl")

        self.documenn_index_info = input

        if not self.redis.exists_with_key_type(
            input.user_properties, RedisKeyType.VECTORSTORE
        ):
            logger.info(
                f"Saving index for: {input.user_properties.user_id}:{input.user_properties.session_id}"
            )
            self.redis.safe_set_with_key_type(
                input.user_properties, RedisKeyType.VECTORSTORE, []
            )
        vectorstore = self.redis.safe_get_with_key_type(
            input.user_properties, RedisKeyType.VECTORSTORE
        )
        new_vectorstore = []
        for index_info_json in vectorstore:
            index_info = DocumentIndexInfo(**json.loads(index_info_json))
            if index_info.index_id == input.index_id:
                logger.info(f"Index {input.index_id} already exists.")
                continue
            new_vectorstore.append(index_info_json)
        new_vectorstore.append(input.json())
        self.redis.safe_set_with_key_type(
            input.user_properties, RedisKeyType.VECTORSTORE, new_vectorstore
        )
        return input

    def similarity_search(self, input: SimilaritySearchInput):
        if self.index is None:
            logger.error("Index must be loaded before performing similarity search.")
            return None
        return self.index.similarity_search(query=input.query, k=input.k)

    def remove_index(self):
        if self.index is None:
            logger.error("Index must be loaded before removing.")
            return None

        if not self.redis.exists_with_key_type(
            self.documenn_index_info.user_properties,
            RedisKeyType.VECTORSTORE,
        ):
            logger.info(f"Index {self.documenn_index_info.index_name} does not exist.")
            return

        if (
            isinstance(self.documenn_index_info.connection, str)
            and self.documenn_index_info.connection == "local"
        ):
            logger.info("Removing index from local.")
            os.remove(self.documenn_index_info.index_path)
            os.remove(self.documenn_index_info.index_pkl_path)

        all_document_index_info = self.redis.safe_get_with_key_type(
            self.documenn_index_info.user_properties,
            RedisKeyType.VECTORSTORE,
        )
        processed_document_index_info = []
        for doc_json in all_document_index_info:
            doc = DocumentIndexInfo(**json.loads(doc_json))
            if doc.index_id != self.documenn_index_info.index_id:
                processed_document_index_info.append(doc_json)

        self.redis.safe_set_with_key_type(
            self.documenn_index_info.user_properties,
            RedisKeyType.VECTORSTORE,
            processed_document_index_info,
        )

        self.index = None
        self.documenn_index_info = None
