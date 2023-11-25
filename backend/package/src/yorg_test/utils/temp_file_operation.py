import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Any, List
from typing import IO

FILE_CONNECTOR_TMP_STORAGE_PATH = os.environ.get(
    "FILE_CONNECTOR_TMP_STORAGE_PATH", "/knowledge_base"
)
_FILE_AGE_CLEANUP_THRESHOLD_HOURS = 24 * 7  # 1 week
_VALID_FILE_EXTENSIONS = [".txt", ".zip", ".pdf"]


def get_file_ext(file_path_or_name: str | Path) -> str:
    _, extension = os.path.splitext(file_path_or_name)
    return extension


def check_file_ext_is_valid(ext: str) -> bool:
    return ext in _VALID_FILE_EXTENSIONS


def write_temp_files(
    user_id: str,
    files: list[tuple[str, IO[Any]]],
    base_path: Path | str = FILE_CONNECTOR_TMP_STORAGE_PATH,
) -> list[str]:
    """Writes temporary files to disk and returns their paths

    NOTE: need to pass in (file_name, File) tuples since FastAPI's `UploadFile` class
    exposed SpooledTemporaryFile does not include a name.
    """
    file_location = Path(base_path) / user_id / str(uuid.uuid4())
    os.makedirs(file_location, exist_ok=True)

    file_paths: list[str] = []
    for file_name, file in files:
        extension = get_file_ext(file_name)
        if not check_file_ext_is_valid(extension):
            raise ValueError(
                f"Invalid file extension for file: '{file_name}'. Must be one of {_VALID_FILE_EXTENSIONS}"
            )

        file_path = file_location / file_name
        with open(file_path, "wb") as buffer:
            # copy file content from uploaded file to the newly created file
            shutil.copyfileobj(file, buffer)

        file_paths.append(str(file_path.absolute()))

    return file_paths


def file_age_in_hours(filepath: str | Path) -> float:
    return (time.time() - os.path.getmtime(filepath)) / (60 * 60)


def clean_old_temp_files(
    files_path: List[str],
) -> None:
    # os.makedirs(Path(base_path) / user_id, exist_ok=True)
    for file in files_path:
        # if file_age_in_hours(Path(base_path) / file) > age_threshold_in_hours:
        #     os.remove(Path(base_path) / user_id / file)
        os.remove(file)
