from typing import Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from markdown import markdown

import json

from ipykernel.kernelbase import Kernel
from ipykernel.comm import Comm

import ipywidgets as widgets


class HandlerInput(BaseModel):
    cell_type: str = Field(description="Cell type")
    code: str = Field(description="Code to execute")
    cell_id: Optional[str] = Field(description="Cell ID")
    yorg_upload_files: Optional[list] = Field(description="User Upload Files")


class Handler(ABC):
    _instance = None

    def __new__(cls, kernel: Kernel):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    @abstractmethod
    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        pass

    @abstractmethod
    def do_shutdown(self, restart: bool):
        pass

    def _send_comm_obj(self, target_name: str, data: any):
        self.kernel._send_comm_obj(target_name, data)

    def _send_comm_model(self, target_name: str, data: BaseModel):
        self.kernel._send_comm_model(target_name, data)

    def _send_widget(self, widget: widgets.Widget):
        self.kernel._send_widget(widget)

    def _send_markdown(self, content: str):
        self.kernel._send_markdown(content)
