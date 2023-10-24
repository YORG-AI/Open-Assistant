from pydantic import BaseModel

class DocumentInput(BaseModel):
    document_id: str

class CreateDocumentInput(BaseModel):
    title: str

class DeleteDocumentInput(BaseModel):
    document_id: str

class SheetInput(BaseModel):
    document_id: str
    sheet_id: str

class AppendOrUpdateInput(BaseModel):
    document_id: str
    sheet_id: str
    data: list[list[str]]

class ClearSheetInput(BaseModel):
    document_id: str
    sheet_id: str

class CreateSheetInput(BaseModel):
    document_id: str
    title: str

class DeleteColumnsOrRowsInput(BaseModel):
    document_id: str
    sheet_id: str
    start_index: int
    end_index: int
    dimension: str  # Either 'ROWS' or 'COLUMNS'

class ReadRowsInput(BaseModel):
    document_id: str
    sheet_id: str

class RemoveSheetInput(BaseModel):
    document_id: str
    sheet_id: str

class UpdateRowsInput(BaseModel):
    document_id: str
    sheet_id: str
    data: list[list[str]]
