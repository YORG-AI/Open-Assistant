SDE_PROMPT = """
You are a software engineer working on a project. You are working on a feature implementation task.

"""

REPO_STRUCTURE_PROMPT = """
The project has a file tree structure as follows:

```text
{file_tree}
```

"""

FEATURE_PROMPT = """
Now you are assigned to implement a feature, which is described as follows:

{feature_description}

"""

FOCUS_FILE_PATH_PROMPT = """
Now please provide a list of file paths that you think are relevant to this feature implementation task. 
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
Focus files is a list of files that you should focus on for this feature implementation task. 
You should modify these files (or add new file) to implement the feature.
The list of focus files is as follows:

{focus_files}
"""

PLAN_PROMPT = """
Please design a high level plan for this feature implementation task.
Your output should be a title (`## plan`, attention: lower case) and python list of modification plans. The example output is as follows:

{format_example}

---

IF YOU THINK YOU DON'T NEED TO MODIFY A SPECIFIC FILE, YOU SHOULDN'T INCLUDE IT IN YOUR OUTPUT.
DO NOT INCLUDE ANY OTHER INFORMATION IN YOUR OUTPUT.
"""

PLAN_FORMAT_EXAMPLE = """
## plan
```python
[
    ("add", "path/to/file1", "the reason why you want to add this file"),
    ("remove","path/to/file2", "the reason why you want to remove this file"),
    ("modify", "path/to/file3", "the detailed plan for modification"),
    ("modify","path/to/file4", "the detailed plan for modification"),
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
