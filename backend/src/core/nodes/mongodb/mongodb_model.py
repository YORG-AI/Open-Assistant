from pydantic import BaseModel
from typing import List, Dict


class AggregateInput(BaseModel):
    collection_name: str
    pipeline: list


class DeleteInput(BaseModel):
    collection_name: str
    query: dict


class FindInput(BaseModel):
    collection_name: str
    query: dict
    projection: dict = None


class FindReplaceInput(BaseModel):
    collection_name: str
    filter: dict
    replacement: dict


class FindUpdateInput(BaseModel):
    collection_name: str
    filter: dict
    update: dict


class InsertInput(BaseModel):
    collection_name: str
    documents: List[Dict]


class UpdateInput(BaseModel):
    collection_name: str
    filter: dict
    update: dict
