from fastapi.testclient import TestClient
from src.main import app
from src.core.nodes.document_loader.document_model import (
    Document,
    SplitDocumentInput,
    DEFAULT_DOCUMENTS_FOLDER,
)
from src.core.common_models import (
    UserProperties,
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID,
    RedisKeyType,
    DEFAULT_GIT_FOLDER,
)
from src.core.nodes.document_loader.document_loader import DocumentLoaderNode
from src.service.redis import Redis
from pathlib import Path
import json


def test_create_document_from_file():
    """
    Test function to check if the default upload file is working as expected.
    """
    for extension in ("pdf", "txt", "docx", "csv"):
        _test_upload_file = Path(
            "src/data/tests", f"document_loader_test_sample.{extension}"
        )
        _files = {"input": _test_upload_file.open("rb")}
        with TestClient(app) as client:
            response = client.post(
                "nodes/document_loader/create_document_from_file", files=_files
            )
            assert response.status_code == 200
            response_json = json.loads(response.json())
            document = Document(**response_json)

            assert document.user_properties.user_id == DEFAULT_USER_ID
            assert document.user_properties.session_id == DEFAULT_SESSION_ID
            assert (
                document.file_path
                == DEFAULT_DOCUMENTS_FOLDER
                / DEFAULT_USER_ID
                / DEFAULT_SESSION_ID
                / document.file_name
            )
            assert (
                document.file_name
                == f"{document.creation_time}-document_loader_test_sample.{extension}"
            )
            assert document.file_extension == extension
            assert len(document.documents) > 0

            # test if document is save in redis
            redis = Redis()
            all_documents = redis.safe_get_with_key_type(
                document.user_properties, RedisKeyType.DOCUMENTS
            )
            exist = False
            for doc_json in all_documents:
                doc = Document(**json.loads(doc_json))
                if doc.file_id == document.file_id:
                    exist = True
                    assert doc.file_id == document.file_id
                    assert doc.file_path == document.file_path
                    assert doc.file_name == document.file_name
                    assert doc.file_extension == document.file_extension
                    assert doc.file_size == document.file_size
                    assert doc.creation_time == document.creation_time
                    assert doc.documents == document.documents
            assert exist is True

            DocumentLoaderNode().remove_document(input=document)


def test_create_document_from_url():
    with TestClient(app) as client:
        response = client.post(
            "nodes/document_loader/create_document_from_url",
            json={
                "input": {
                    "url": "https://github.com/geekan/MetaGPT",
                    "type": "git",
                },
                "properties": {
                    "user_id": DEFAULT_USER_ID,
                    "session_id": DEFAULT_SESSION_ID,
                },
            },
        )
        assert response.status_code == 200
        response_json = json.loads(response.json())
        document = Document(**response_json)

        assert document.user_properties.user_id == DEFAULT_USER_ID
        assert document.user_properties.session_id == DEFAULT_SESSION_ID
        assert document.file_name == "https://github.com/geekan/MetaGPT"
        assert document.file_extension == "git"
        assert len(document.documents) > 0

        # test if document is save in redis
        redis = Redis()
        all_documents = redis.safe_get_with_key_type(
            document.user_properties, RedisKeyType.DOCUMENTS
        )
        exist = False
        for doc_json in all_documents:
            doc = Document(**json.loads(doc_json))
            if doc.file_id == document.file_id:
                exist = True
                assert doc.file_id == document.file_id
                assert doc.file_name == document.file_name
                assert doc.file_extension == document.file_extension
                assert doc.creation_time == document.creation_time
                assert doc.documents == document.documents
        assert exist is True

        DocumentLoaderNode().remove_document(input=document)

        # test web loader
        response = client.post(
            "nodes/document_loader/create_document_from_url",
            json={
                "input": {
                    "url": "https://www.espn.com/",
                    "type": "web",
                },
                "properties": {
                    "user_id": DEFAULT_USER_ID,
                    "session_id": DEFAULT_SESSION_ID,
                },
            },
        )
        assert response.status_code == 200
        response_json = json.loads(response.json())
        document = Document(**response_json)

        assert document.user_properties.user_id == DEFAULT_USER_ID
        assert document.user_properties.session_id == DEFAULT_SESSION_ID
        assert document.file_name == "https://www.espn.com/"
        assert document.file_extension == "web"
        assert len(document.documents) > 0

        # test if document is save in redis
        redis = Redis()
        all_documents = redis.safe_get_with_key_type(
            document.user_properties, RedisKeyType.DOCUMENTS
        )
        exist = False
        for doc_json in all_documents:
            doc = Document(**json.loads(doc_json))
            if doc.file_id == document.file_id:
                exist = True
                assert doc.file_id == document.file_id
                assert doc.file_name == document.file_name
                assert doc.file_extension == document.file_extension
                assert doc.creation_time == document.creation_time
                assert doc.documents == document.documents
        assert exist is True

        DocumentLoaderNode().remove_document(input=document)


def test_split_documents():
    """
    Test function to check if the split documents function is working as expected.
    """
    _test_upload_file = Path("src/data/tests", "document_loader_test_sample.pdf")
    _files = {"input": _test_upload_file.open("rb")}
    with TestClient(app) as client:
        response = client.post(
            "nodes/document_loader/create_document_from_file", files=_files
        )
        assert response.status_code == 200
        response_json = json.loads(response.json())
        document = Document(**response_json)
        split_document_input = SplitDocumentInput(
            file_id=document.file_id, chunk_size=1000, chunk_overlap=100
        )
        response = client.post(
            "nodes/document_loader/split_documents", json=split_document_input.dict()
        )

        assert response.status_code == 200
        assert len(response.json()) == 23

        DocumentLoaderNode().remove_document(input=document)
