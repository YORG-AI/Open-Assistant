import fire
import asyncio
import inquirer
from rich.markdown import Markdown
from rich import print as rprint

import src.interaction.software_engineer as software_engineer
import src.interaction.data_analysis as data_analysis
import src.interaction.git_repo as git_repo

from src.utils.interaction import user_list

from dotenv import load_dotenv


load_dotenv()


async def startup(model: str):
    welcome_message = "Starting code interpreter..."
    welcome_message += f"\n> Model set to `{model}`"
    rprint(Markdown(welcome_message), "")

    mode = user_list(
        "Select the software development",
        ["data_analysis", "git_repo", "software_engineer"],
    )

    if mode == "git_repo":
        await git_repo.run()
    elif mode == "data_analysis":
        await data_analysis.run()
    elif mode == "software_engineer":
        await software_engineer.run()


def main(
    model: str = "gpt-4",
):
    asyncio.run(startup(model))


if __name__ == "__main__":
    fire.Fire(main)
