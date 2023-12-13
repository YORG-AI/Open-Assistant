from pydantic import BaseModel
from pathlib import Path

from typing import Optional
from enum import Enum
import json

DEFAULT_DOCUMENTS_FOLDER = Path("src/data/documents/")
DEFAULT_GIT_FOLDER = Path("src/data/git/")
DEFAULT_DATA_ANALYSIS_FOLDER = Path("src/data/data_analysis/")
DEFAULT_USER_ID = "admin"
DEFAULT_SESSION_ID = "admin_session"
TIME_STRING_FORMAT = "%Y-%m-%d-%H:%M:%S"


class RedisKeyType(Enum):
    """
    An enumeration for Redis key types.
    """

    DOCUMENTS = "documents"
    VECTORSTORE = "vectorstore"


class UserProperties(BaseModel):
    user_id: Optional[str] = DEFAULT_USER_ID
    session_id: Optional[str] = DEFAULT_SESSION_ID

    def generate_redis_key_with_type(self, key_type: RedisKeyType):
        return f"{self.user_id}:{self.session_id}:{key_type.value}"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
