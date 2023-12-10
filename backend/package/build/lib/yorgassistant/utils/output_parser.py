import re
import ast
import typeguard

from abc import ABC, abstractmethod, abstractclassmethod
from subprocess import CompletedProcess


class Block(ABC):
    def __init__(self, text: str, title: str):
        self.raw_text = text
        self.title = title

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def content(self):
        pass


class CodeBlock(Block):
    CODE_BLOCK_PATTERN = r"```{lang}.*?\s+(.*?)\s+```"

    def __init__(self, text: str, title: str, lang: str = ""):
        super().__init__(text, title)
        self.lang = lang
        self.code = ""

    def parse(self):
        pattern = self.CODE_BLOCK_PATTERN.format(lang=self.lang)
        match = re.search(pattern, self.raw_text, re.DOTALL)
        if match:
            self.code = match.group(1)
        else:
            raise Exception(
                f"Cannot parse {self.lang} code block in text: \n{self.raw_text}"
            )

    def content(self):
        return self.code


class PythonCodeBlock(CodeBlock):
    def __init__(self, text: str, title: str):
        super().__init__(text, title, lang="python")
        self.pyobj = None

    def parse(self):
        super().parse()
        if not self._is_valid_python(self.code):
            raise Exception(f"Code block is not valid python: {self.code}")
        else:
            try:
                self.pyobj = ast.literal_eval(self.code)
            except Exception as e:
                raise Exception(
                    f"Cannot parse python code block: {self.code}, error: {e}"
                )

    def content(self):
        return self.pyobj

    def _is_valid_python(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False


class StringBlock(Block):
    def __init__(self, text: str, title: str):
        super().__init__(text, title)
        self.text = ""

    def parse(self):
        self.text = self.raw_text

    def content(self):
        return self.text


# Output Converter Class:
#


class OuptutParser(ABC):
    @classmethod
    @abstractclassmethod
    def parse_output(cls, input):
        pass

    @classmethod
    @abstractclassmethod
    def parse_output_with_schema(cls, input, schema):
        pass


class LLMOutputParser(OuptutParser):
    """
    input: str -> output: dict[str, any]
    """

    @classmethod
    def parse_output(cls, input: str) -> dict[str, any]:
        block_dict = {}

        block_texts = cls._split_block_text(input)
        for block_text in block_texts:
            block_title, block_content = block_text
            block = cls._parse_block(block_content, block_title)
            block.parse()
            content = block.content()
            block_dict[block_title] = content
        return block_dict

    @classmethod
    def parse_output_with_schema(
        cls, input: str, schema: dict[str, type]
    ) -> dict[str, any]:
        block_dict = {}

        block_texts = cls._split_block_text(input)
        for block_text in block_texts:
            block_title, block_content = block_text

            if block_title in schema.keys():
                block = cls._parse_block(block_content, block_title)
                block.parse()
                content = block.content()
                try:
                    content = typeguard.check_type(content, schema[block_title][0])
                    block_dict[block_title] = content
                except Exception as e:
                    raise Exception(f"Parse {block_title} error: {e}")

        return block_dict

    @classmethod
    def _split_block_text(cls, text: str) -> list[tuple[str, str]]:
        block_texts = text.split("##")
        block_list = []
        for block_text in block_texts:
            block_text = block_text.strip()
            if block_text != "":
                try:
                    block_title, block_content = block_text.split("\n", 1)
                except Exception as e:
                    raise Exception(f"Cannot split block text: {block_text}, error: {e}")
                block_title.strip()
                block_content.strip()
                block_list.append((block_title, block_content))
        return block_list

    @classmethod
    def _parse_block(cls, block_content: str, block_title: str) -> Block:
        if block_content.startswith("```python"):
            return PythonCodeBlock(block_content, block_title)
        else:
            return Block(block_content, block_title)


class RawOutputParser(OuptutParser):
    """
    input: any -> output: any
    """

    @classmethod
    def parse_output(cls, input: any) -> any:
        return input

    @classmethod
    def parse_output_with_schema(
        cls, input: any, _: any
    ) -> any:
        return input

class GitLoaderOutputParser(OuptutParser):
    @classmethod
    def parse_output_with_schema(
        cls, text: str, schema: dict[str, type]
    ) -> dict[str, any]:

        code_content = PythonCodeBlock(text, "code").parse()
        return {"Code Content": code_content}
