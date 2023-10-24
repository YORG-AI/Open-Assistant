import os
from rich.markdown import Markdown
from rich import print as rprint

from src.core.assignments.code_interpreter.code_interpreter import (
    CodeInterpreterAssignment,
    CodeInterpreterInput,
    CodeInterpreterOutput,
    ActionType,
)
from src.core.common_models import (
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID,
)
from src.utils.interaction import user_input, user_confirm, user_checkbox


# Convert history to markdown format
def history_to_markdown(history):
    markdown_string = ""
    for entry in history:
        role = entry["role"]
        content = entry["content"]
        if role == "user":
            markdown_string += f"> **{role.capitalize()}**: {content}\n\n"
        else:  # Assistant or other roles
            markdown_string += f"**{role.capitalize()}**: {content}\n\n"
    return markdown_string


async def run():
    # Init code interpreter
    code_interpreter = CodeInterpreterAssignment()

    # Specify the folder path
    folder_path = f"src/data/documents/{DEFAULT_USER_ID}/{DEFAULT_SESSION_ID}"

    # Get all .csv and .json files under the given folder path
    files = [f for f in os.listdir(folder_path) if f.endswith((".csv", ".json"))]

    # Create a list of choices for inquirer.List
    choices = [{"name": f, "value": os.path.join(folder_path, f)} for f in files]

    selected_files = user_checkbox("Select one or more files", choices)

    for file_info in selected_files:
        code_interpreter_input = CodeInterpreterInput(
            type=ActionType.FILE,
            content=file_info["value"],
        )
        code_interpreter_output = await code_interpreter.run(code_interpreter_input)
        code_interpreter_output_formatted_output: CodeInterpreterOutput = (
            code_interpreter_output.formatted_output
        )
        rprint(
            Markdown(
                history_to_markdown(code_interpreter_output_formatted_output.history)
            ),
            "",
        )

    # query loop
    while True:
        query = user_input("please enter your query")
        if query == "exit":
            break
        code_interpreter_input = CodeInterpreterInput(
            type=ActionType.QUERY,
            content=query,
        )
        code_interpreter_output = await code_interpreter.run(code_interpreter_input)
        code_interpreter_output_formatted_output: CodeInterpreterOutput = (
            code_interpreter_output.formatted_output
        )

        for message in code_interpreter_output_formatted_output.history:
            role = message["role"]
            if role == "user":
                rprint(Markdown(f"> **{role.capitalize()}** \n"), "")
            else:
                rprint(Markdown(f"**{role.capitalize()}** \n"), "")
            rprint(Markdown(f"{message['content']}\n\n"), "")
