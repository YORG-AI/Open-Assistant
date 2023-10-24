from tqdm import tqdm
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress
from rich import print as rprint

from src.core.agents import SoftwareEngineerAgent, Plan

from src.utils.interaction import user_input, user_confirm, user_list


async def run():
    # User input repo url and feature description
    repo_url = user_input("Please provide the repo url")

    # Set feature description
    feature_text = user_input("Please provide the feature description")

    # Create agent
    agent = SoftwareEngineerAgent()

    agent.set_repo_url(repo_url)
    agent.set_feature_description(feature_text)
    agent.set_focus_files()

    print("LLM is thinking...")

    # Get focus files
    focus_files = list(agent.get_focus_files())
    print(
        "LLM think the files that are relative to the feature implementation are as follows:"
    )
    for path in focus_files:
        print("- " + path)

    # User modify focus_files
    need_modify = user_confirm("Do you want to modify the focus files?")
    while need_modify:
        target = user_list(
            "Choose a file to remove / Add a new file",
            list(agent.get_focus_files()) + ["Add new file", "Stop modifying"],
        )
        if target == "Add new file":
            # User add a new file
            target = user_input("Please provide the file path")
            agent.add_focus_file(target)
        elif target == "Stop modifying":
            break
        else:
            # User remove a file
            do_remove = user_confirm(
                "Do you want to remove this file from focus file list?"
            )
            if do_remove:
                agent.remove_focus_file(target)
        need_modify = user_confirm("Continue modify the focus files?", default=True)

    print("Final focus files:")
    for path in agent.get_focus_files():
        print("- " + path)

    print("LLM is planning the implementation...")

    # Design plan
    agent.design_plan()

    # Get the plan
    plans = agent.get_plan()
    print("LLM think the implementation plan is as follows:")
    for plan in plans:
        rprint(Markdown(f"{plan.to_markdown()}"), "")

    # User modify plan
    need_modify = user_confirm("Do you want to modify the plan?")
    while need_modify:
        target = user_list(
            "Choose a plan to remove / add a new plan",
            agent.get_plan() + ["Add new plan", "Stop modifying"],
        )
        if target == "Add new plan":
            # User add a new plan
            action = user_list(
                "Choose a action",
                ["add", "remove", "modify"],
            )
            file_path = user_input("Please provide the file path")
            description = user_input("Please provide the description")
            agent.add_plan(
                Plan(
                    action=action,
                    file_path=file_path,
                    description=description,
                )
            )
        elif target == "Stop modifying":
            break
        else:
            # User remove a plan
            do_remove = user_confirm("Do you want to remove this plan?")
            if do_remove:
                agent.remove_plan(target)

        need_modify = user_confirm("Continue modify the plan?")

    print("Final plan:")
    for plan in agent.get_plan():
        rprint(Markdown(f"{plan.to_markdown()}"), "")

    # Implement the plan
    print("LLM starts implementing all the plan.")
    with Progress() as progress:
        task = progress.add_task(
            "Implementing all plans...", total=len(agent.get_plan())
        )
        for action in progress.track(agent.implement(), task_id=task):
            rprint(Markdown(f"{action}", ""))

    # User confirm the file actions
    apply = user_confirm("Do you want to apply the modifications?")
    if apply:
        agent.apply_file_action()
        print("LLM has applied the modifications.")
