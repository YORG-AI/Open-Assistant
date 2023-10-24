from __future__ import annotations

import asyncio

from abc import ABC, abstractmethod
from typing import Type, Optional
from pydantic import BaseModel, create_model, Field

from src.core.nodes.base_node import BaseNode
from src.utils.output_parser import OuptutParser


class AssignmentConfig(BaseModel):
    name: str = Field(description="Assignment 名称")
    description: str = Field(default="", description="Assignment 描述")


class BaseAssignment(ABC):
    AssignmentConfig: AssignmentConfig

    nodes: dict[str, BaseNode]
    output: AssignmentOutput


class AssignmentOutput:
    name: str

    output_schema: Optional[dict[str, tuple]]
    output_type: Type[BaseModel]

    raw_output: any
    formatted_output: BaseModel

    parser: OuptutParser

    def __init__(
        self, name: str, output_schema: Optional[dict[str, type]], parser: OuptutParser
    ):
        self.name = name
        self.output_schema = output_schema
        self.parser = parser

    def load(self, raw_text: any):
        self.raw_output = raw_text

        model_class = create_model(self.name, **self.output_schema)
        if self.output_schema is None:
            blocks = self.parser.parse_output(self.raw_output)
        else:    
            blocks = self.parser.parse_output_with_schema(
                self.raw_output, self.output_schema
            )

        self.formatted_output = model_class(**blocks)
