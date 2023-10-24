from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List, Optional
from enum import Enum
import json
import re
import subprocess

from .load_github_repo_prompt import *
from ..base_assignment import BaseAssignment, AssignmentOutput, AssignmentConfig

from src.core.nodes.base_node import NodeInput
from src.core.nodes import (
    DataAnalysisNode,
    LoadDataInput,
    OpenAINode,
    ChatInput,
    CodeRunnerNode,
    RunCodeInput,
    RunCodeFromFileInput,
    DocumentLoaderNode,
    FaissVectorStoreNode,
)
from src.core.common_models import (
    UserProperties,
    RedisKeyType,
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID,
    DEFAULT_GIT_FOLDER,
)
from src.core.nodes.vectorstore.vectorstore_model import (
    SimilaritySearchInput,
    AddIndexInput,
    DocumentIndexInfo,
)
from src.core.nodes.document_loader.document_model import (
    Document,
    SplitDocumentInput,
    UrlDocumentInput,
)
from src.core.nodes.openai.openai_model import OpenAIResp
from src.core.nodes.openai.openai_model import ChatInput
from src.utils.output_parser import GitLoaderOutputParser, PythonCodeBlock
from src.utils.router_generator import generate_assignment_end_point
from dotenv import load_dotenv

load_dotenv()


class Mode(str, Enum):
    FEATURE_IMPLEMENTATION = "feature_implementation"
    FIX_BUGS = "fix_bugs"
    SIMILARITY_SEARCH = "similarity_search"


class LoadGithubRepoInput(BaseModel):
    query: str = Field(description="Query for searching github repo.")
    top_k: Optional[int] = Field(5, description="Top k for searching github repo.")
    target_files: Optional[List[str]] = Field(
        [], description="Target files for searching github repo."
    )
    error_message: Optional[str] = Field(description="Error message for fixing bugs.")
    mode: Mode = Field(default=Mode.SIMILARITY_SEARCH, description="Mode for input.")


load_github_repo_config = {
    "name": "load_github_repo",
    "description": "Load github repo and ask questions",
}


@generate_assignment_end_point
class LoadGithubRepoAssignment(BaseAssignment):
    config: AssignmentConfig = AssignmentConfig(**load_github_repo_config)
    document: Document = None
    document_index_info: DocumentIndexInfo = None

    def __init__(self):
        self.chat_node = OpenAINode()
        self.code_runner_node = CodeRunnerNode()
        self.document_loader_node = DocumentLoaderNode()
        self.faiss_vectorstore_node = FaissVectorStoreNode()

        self.nodes = {
            "openai": self.chat_node,
            "code_runner": self.code_runner_node,
            "document_loader": self.document_loader_node,
            "faiss_vectorstore": self.faiss_vectorstore_node,
        }
        self.output = AssignmentOutput(
            "load_github_repo",
            OUTPUT_SCHEMA,
            GitLoaderOutputParser,
        )

    def init_document(self, repo_url: str):
        response = self.document_loader_node.create_document_from_url(
            input=UrlDocumentInput(
                url=repo_url,
                type="git",
            ),
            properties=UserProperties(),
        )
        document = Document(**json.loads(response))
        self.document = document

    def init_vectorstore(self, chunk_size: int = 200, chunk_overlap: int = 0):
        add_index_input = AddIndexInput(
            user_properties=UserProperties(
                user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID
            ),
            split_documents=[
                SplitDocumentInput(
                    file_id=self.document.file_id,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            ],
        )

        document_index_info: DocumentIndexInfo = self.faiss_vectorstore_node.add_index(
            add_index_input
        )

        self.document_index_info = document_index_info

    def update_file_content(self, file_path, file_content):
        with open(self.document.file_path / file_path, "w") as f:
            # Identify the minimum indentation across all non-empty lines
            min_indent = min(
                len(re.match(r"^\s*", line).group())
                for line in file_content.splitlines()
                if line.strip()
            )

            # Remove the minimum indentation from each line
            adjusted_content_lines = [
                line[min_indent:] for line in file_content.splitlines()
            ]

            # Strip trailing whitespace from each line
            stripped_adjusted_lines = [line.rstrip() for line in adjusted_content_lines]

            # Join the adjusted lines to form the final content
            final_content = "\n".join(stripped_adjusted_lines)

            f.write(final_content)

    def run_script(self, file_path):
        run_code_input = RunCodeFromFileInput(
            working_dir=str(self.document.file_path),
            file_path=file_path,
        )
        output = self.code_runner_node.run_code_from_file(run_code_input)
        return output

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def run(self, input: LoadGithubRepoInput):
        match input.mode:
            case Mode.FEATURE_IMPLEMENTATION:
                content = ""
                for target_file in input.target_files:
                    content += f"This is the path to file {target_file}\n"
                    content += f"This is file content\n"

                    with open(self.document.file_path / target_file, "rb") as f:
                        target_file_content = f.read()
                        content += f"{target_file_content} \n\n"

                prompt = FEATURE_IMPLEMENTATION_PROMPT_TEMPLATE.format(
                    content=content,
                    feature_requirement=input.query,
                    format_example=FORMAT_EXAMPLE,
                )
            case Mode.FIX_BUGS:
                content = ""
                for target_file in input.target_files:
                    content += f"This is the path to file {target_file}\n"
                    content += f"This is file content\n"

                    with open(self.document.file_path / target_file, "rb") as f:
                        target_file_content = f.read()
                        content += f"{target_file_content} \n\n"

                    prompt = FIX_BUGS_PROMPT_TEMPLATE.format(
                        content=content,
                        error_message=input.error_message,
                        format_example=FORMAT_EXAMPLE,
                    )
            case Mode.SIMILARITY_SEARCH:
                top_k = self.faiss_vectorstore_node.similarity_search(
                    SimilaritySearchInput(query=input.query, k=input.top_k)
                )

                prompt = PROMPT_TEMPLATE.format(
                    content=top_k,
                    question=input.query,
                )

        node_input = NodeInput(
            func_name="chat",
            func_input=ChatInput(
                model="gpt-4",
                message_text=prompt,
            ),
        )

        text_output: OpenAIResp = self.nodes["openai"].run(node_input)
        if input.mode is Mode.SIMILARITY_SEARCH:
            return text_output
        code_block = PythonCodeBlock(text_output.message.content, "code")
        code_block.parse()
        return code_block.content()
