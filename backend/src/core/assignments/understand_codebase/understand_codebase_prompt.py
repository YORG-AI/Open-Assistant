CODEBASE_PROMPT = """
[Role]: You are an expert in software development and you are helping a junior developer understand a codebase. You will be provided with some
related context (some including code) of the question, please answer the question appropriately.
[Requirement]: Your answer should just give me the output without any prefix like 'Output:' or 'Answer:'.


"""

REPO_STRUCTURE_PROMPT = """
The project has a file tree structure as follows:

```text
{file_tree}
```

"""

FILE_DEPENDENCIES_PROMPT = """
The following provided is the project dependencies, there is a template below help you understand the dependenies:

{dependencies_template}

The project has the dependencies as follows:

```text
{file_dependencies}
```

"""

FILE_CLASSES_PROMPT = """
The following provided is the project file classes, there is a template below help you understand:

{classes_template}

The project's .py file has the classes as follows:

```text
{file_classes}
```

"""

DEPENDENCIES_TEMPLATE = """
{
    '/path/to/my_project/file1': [file1's related file],
    '/path/to/my_project/file2': [file2's related file],
    '/path/to/my_project/file3': [file3's related file]
}
"""

CLASSES_TEMPLATE = """
{
    '/path/to/my_project/file1': [file1's classes],
    '/path/to/my_project/file2': [file2's classes],
    '/path/to/my_project/file3': [file3's classes]
}
"""

SET_FEATURE_PROMPT = """
The code user does query is attached below:

{query_related_code}

If the user query is empty , that means you only need to explain the usage of the code in the whole codebase
The query which the user most concerned about understand codebase is as below:

{user_feature}

and the following is the content of pm spec and requirements which related to the features:

{related_content}

"""

FOCUS_FILE_PATH_PROMPT = """
According to the file tree, file dependencies, file classes, and the related content of files provided before,
please provide a list of file paths that you think are relevant to user's query and the code user has provided. 
If there are more than 5 relevant files, you should only provide top 5 files.

Your output should be a title (`##files`, attention: lower case) and a python code block, which include a list of file paths (you are allow to create new files). The example output is as follows:

{format_example}

---

YOU SHOULD ONLY OUTPUT EXISTING FILE PATHS IN THE REPO.
DO NOT INCLUDE ANY OTHER INFORMATION IN YOUR OUTPUT.
YOU SHOULD ONLY OUTPUT TOP 5 FILES.
"""


FOCUS_FILE_PATH_EXAMPLE = """
## files
```python
[
    "path/to/file1", 
    "path/to/file2", 
    "path/to/file3",
]
```
"""

FOCUS_FILE_PROMPT = """
Focus files is a list of files that you should focus on for this understand codebase task. 
You should carefully analysis the code and provide the understanding.
The list of focus files is as follows:

{focus_files}

"""

UNDERSTANDING_CODEBASE_PROMPT = """
Please according to the code and query user provided before to provide a high level understanding for these focus files. 
Your output should be a title (`## understanding`, attention: lower case) and python list of modification plans. 
The example output is as follows:

{format_example}

---

"""

UNDERSTANDING_CODEBASE_TEMPLATE = """
## understanding
```python
[
    ("path/to/file1","the related code content in file1", "the understanding of file1"),
    ("path/to/file2","the related code content in file2", "the understanding of file2"),
    ("path/to/file3","the related code content in file3", "the understanding of file3"),
    ...
]
"""

ADD_FILE_PROMPT = """
The path of the file to be added is {file_path}.

The detailed description of the file to be added is as follows:

{action_description}

Please write the file content for me. The output should only be a python string of file content.
DO NOT INCLUDE ANY OTHER INFORMATION EXCEPT THE FILE CONTENT IN YOUR OUTPUT.
"""

MODIFY_FILE_PROMPT = """
The path of the file to be modified is {file_path}, and the content of the file is as follows:

{file_content}

The detailed description of the file to be modified is as follows:

{action_description}

Please write the file content for me. The output should only contain file content.

---

DO NOT CONTAIN QUOTATION MARKS (\", \"\"\", \', etc.) AT THE BEGINNING AND THE END OF THE FILE CONTENT.
YOUR OUTPUT SHOULD JUST USE `\n` FOR LINE BREAK, DO NOT USE `\\n`.
DO NOT INCLUDE ANY OTHER INFORMATION EXCEPT FOR THE FILE CONTENT IN YOUR OUTPUT.
"""
