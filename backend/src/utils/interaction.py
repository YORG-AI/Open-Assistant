import inquirer



def user_input(message: str, prefix=">>> ", arg_type=str):
    questions = inquirer.Text("_arg", message=prefix + message)
    return arg_type(inquirer.prompt([questions])["_arg"])


def user_confirm(message: str, prefix=">>> ", default=False) -> bool:
    questions = inquirer.Confirm("_arg", message=prefix + message, default=default)
    return inquirer.prompt([questions])["_arg"]


def user_checkbox(message: str, choices: list, prefix=">>> ") -> list:
    questions = inquirer.Checkbox("_arg", message=prefix + message, choices=choices)
    return inquirer.prompt([questions])["_arg"]

def user_list(message: str, choices: list, prefix=">>> "):
    questions = inquirer.List("_arg", message=prefix + message, choices=choices)
    return inquirer.prompt([questions])["_arg"]