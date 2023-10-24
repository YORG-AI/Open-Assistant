from pydantic import BaseModel

class TranslateInput(BaseModel):
    text: str
    target_language: str
    source_language: str = None  # Optional
