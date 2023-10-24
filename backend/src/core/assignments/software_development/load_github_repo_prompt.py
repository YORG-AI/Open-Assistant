PROMPT_TEMPLATE = """
[Role]: You are an expert in software development and you are helping a junior developer understand a codebase. You will be provided with some
related context (some including code) of the question, please answer the question appropriately.
[Requirement]: Your answer should just give me the output without any prefix like 'Output:' or 'Answer:'.
[Content]: {content}
[Question]: {question}
"""

FEATURE_IMPLEMENTATION_PROMPT_TEMPLATE = """
[Role]: You are an expert in software development and you are helping a junior developer add a new feature. You will be provided with scripts related of the feature requirement,
please modify the scripts and return the code for me
[Content]: {content}
[Feature Requirement]: {feature_requirement}

You should highly obey the type of the example code block, otherwise it will not be able to run.
The content in brackets is just a hint, do not copy them. Don't add any extra text, just follow format.
Your code should be in the following format:

{format_example}
"""

FIX_BUGS_PROMPT_TEMPLATE = """
[Role]: You are an expert in software development and you are helping a junior developer to fix bugs. You will be provided with scripts related of the bug and the error message,
please modify the scripts and return the code for me.
[Content]: {content}
[Error Message]: {error_message}

You should highly obey the type of the example code block, otherwise it will not be able to run.
The content in brackets is just a hint, do not copy them. Don't add any extra text, just follow format.
Your code should be in the following format:

{format_example}
"""


FORMAT_EXAMPLE = """
## Code Content (must be a python list of tuples, each tuple contains two string, first is file path, second is file content)
```python
[
    ("path/to/file", "file_content ..."),
]
```
"""

OUTPUT_SCHEMA = {
    "Code Content": (list[tuple[str, str]], ...),
}
