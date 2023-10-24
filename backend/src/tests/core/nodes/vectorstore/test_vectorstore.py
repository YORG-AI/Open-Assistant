from fastapi.testclient import TestClient
from src.main import app
from src.core.common_models import (
    UserProperties,
    RedisKeyType,
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID,
)
from src.core.nodes.document_loader.document_model import (
    Document,
    SplitDocumentInput,
)
from src.core.nodes.vectorstore.vectorstore_model import (
    SimilaritySearchInput,
    AddIndexInput,
    DocumentIndexInfo,
)
from src.core.nodes.vectorstore.vectorstore import FaissVectorStoreNode
from src.core.nodes.document_loader.document_loader import DocumentLoaderNode
from pathlib import Path
from src.service.redis import Redis
import json


def test_vectorstore():
    for extension in ("pdf", "txt", "docx", "csv"):
        _test_upload_file = Path(
            "src/data/tests", f"document_loader_test_sample.{extension}"
        )
        _files = {"input": _test_upload_file.open("rb")}
        with TestClient(app) as client:
            response = client.post(
                "nodes/document_loader/create_document_from_file",
                files=_files,
                json={
                    "properties": {
                        "user_id": DEFAULT_USER_ID,
                        "session_id": DEFAULT_SESSION_ID,
                    }
                },
            )
            assert response.status_code == 200
            response_json = json.loads(response.json())
            document = Document(**response_json)

            faiss_vector_store_node = FaissVectorStoreNode()

            add_index_input = AddIndexInput(
                user_properties=UserProperties(
                    user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID
                ),
                split_documents=[
                    SplitDocumentInput(
                        file_id=document.file_id, chunk_size=100, chunk_overlap=0
                    )
                ],
            )

            document_index_info: DocumentIndexInfo = faiss_vector_store_node.add_index(
                add_index_input
            )

            assert (
                len(
                    faiss_vector_store_node.similarity_search(
                        SimilaritySearchInput(query="what is the main idea")
                    )
                )
                == 4
            )

            # test if document is save in redis
            redis = Redis()
            all_document_index_info = redis.safe_get_with_key_type(
                UserProperties(user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID),
                RedisKeyType.VECTORSTORE,
            )

            exist = False
            for doc_json in all_document_index_info:
                doc = DocumentIndexInfo(**json.loads(doc_json))
                if doc.index_id == document_index_info.index_id:
                    exist = True
                    assert doc.index_id == document_index_info.index_id
                    assert doc.index_name == document_index_info.index_name
                    assert doc.index_path == document_index_info.index_path
                    assert doc.index_pkl_path == document_index_info.index_pkl_path
                    assert doc.connection == document_index_info.connection
                    assert (
                        doc.segmented_documents
                        == document_index_info.segmented_documents
                    )
            assert exist is True

            faiss_vector_store_node.index = None
            faiss_vector_store_node.documenn_index_info = None

            faiss_vector_store_node.load_index(document_index_info)

            assert faiss_vector_store_node.index is not None
            assert faiss_vector_store_node.documenn_index_info is not None
            assert (
                len(
                    faiss_vector_store_node.similarity_search(
                        SimilaritySearchInput(query="what is the main idea", k=5)
                    )
                )
                == 5
            )

            faiss_vector_store_node.remove_index()

            # test add more index
            faiss_vector_store_node.add_index(add_index_input)
            len_before_add = len(
                faiss_vector_store_node.documenn_index_info.segmented_documents
            )
            faiss_vector_store_node.add_index(add_index_input)
            assert (
                len(faiss_vector_store_node.documenn_index_info.segmented_documents)
                == len_before_add * 2
            )

            faiss_vector_store_node.remove_index()
            DocumentLoaderNode().remove_document(input=document)
