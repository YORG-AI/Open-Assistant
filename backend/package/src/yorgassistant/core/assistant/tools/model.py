from __future__ import annotations  # for type hinting the class itself

from typing import Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field

# model for tool and tool entity


class ObjectType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"


class Schema(BaseModel):
    type: Literal['string', 'number', 'boolean', 'object', 'array'] = Field(description="参数类型")
    description: Optional[str] = Field(description="参数描述")
    properties: Optional[dict[str, Schema]] = Field(description="参数类型为 object 时的元素类型")
    items: Optional[list[Schema]] = Field(description="参数类型为 array 时的元素类型")


class Parameter(BaseModel):
    name: str = Field(description="参数名")
    required: bool = Field(description="是否必须")
    parameter_schema: Schema = Field(description="参数schema")


class Response(BaseModel):
    description: str = Field(description="响应描述")
    content: dict[str, Schema] = Field(description="响应内容")


# model for stateful tool entity

class Stage(BaseModel):
    name: str = Field(description="Stage 名称")
    next_stage_entry: dict[str, list[Parameter]] = Field(
        description="下一个可能的 Stage 名以及对应需要传入的参数列表"
    )
    need_llm_generate_parameters: bool = Field(
        description="在这个 Stage 输入时是否需要 LLM 生成参数"
    )
    need_llm_generate_response: bool = Field(
        description="在这个 Stage 输入时是否需要 LLM 生成回复内容"
    )
