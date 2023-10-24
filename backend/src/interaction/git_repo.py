from rich.markdown import Markdown
from rich import print as rprint

from src.core.assignments.software_development.load_github_repo import (
    LoadGithubRepoAssignment,
    LoadGithubRepoInput,
    Mode,
)

from src.utils.interaction import user_input, user_confirm, user_list


async def understand_codebase(load_github_repo_assignment: LoadGithubRepoAssignment):
    query = user_input("please enter your query")

    load_github_repo_input = LoadGithubRepoInput(
        query=query,
    )

    res = await load_github_repo_assignment.run(load_github_repo_input)
    rprint(Markdown(f"{res.message.content}"), "")


async def feature_implementation(load_github_repo_assignment: LoadGithubRepoAssignment):
    query = user_input("Please enter your feature requirement")
    target_files = user_input(
        "Please enter the path of target files (separated by comma)"
    )

    load_github_repo_input = LoadGithubRepoInput(
        query=query,
        target_files=target_files.split(","),
        mode=Mode.FEATURE_IMPLEMENTATION,
    )

    res = await load_github_repo_assignment.run(load_github_repo_input)

    for file_info in res:
        file_path, file_content = file_info

        rprint(Markdown(f"{file_path}\n\n"), "")
        rprint(Markdown(f"```python {file_content}```\n\n"), "")

        if_apply = user_confirm("Do you want to apply the change to the file?")
        if if_apply:
            load_github_repo_assignment.update_file_content(file_path, file_content)

        test_running_script = user_confirm("Do you want to run the script?")
        if test_running_script:
            need_continue = True

            while need_continue:
                # run script
                output = load_github_repo_assignment.run_script(file_path)

                # if error occurred
                if output.returncode != 0 and len(output.stderr) > 0:
                    print("Exit with code {}, error message:".format(output.returncode))
                    print(output.stderr.decode("utf-8"))

                    fix_error = user_confirm(
                        "It seems that some errors have occurred, do you need to automatically fix them?"
                    )

                    # automatically fix error
                    if fix_error:
                        fix_bug_input = LoadGithubRepoInput(
                            query=query,
                            target_files=target_files.split(","),
                            mode=Mode.FIX_BUGS,
                            error_message=output.stderr.decode("utf-8"),
                        )
                        res = await load_github_repo_assignment.run(
                            fix_bug_input,
                        )
                        file_path, file_content = res[0]
                        rprint(Markdown(f"{file_path}\n\n"), "")
                        rprint(Markdown(f"```python {file_content}```\n\n"), "")

                        if_change = user_confirm(
                            "Do you want to apply the change to the file?"
                        )
                        if if_change:
                            # change file (then run script again)
                            load_github_repo_assignment.update_file_content(
                                file_path, file_content
                            )
                            print("Rerun script...")
                        else:
                            if_stop = user_confirm("Do you want to stop?")
                            if if_stop:
                                need_continue = False
                    else:
                        # do not need to automatically fix error, stop
                        need_continue = False
                else:
                    # no error occurred, stop
                    need_continue = False


async def run():
    repo_url = user_input("Please provide the repo url")

    # init load_github_repo_assignment
    load_github_repo_assignment = LoadGithubRepoAssignment()
    load_github_repo_assignment.init_document(repo_url)
    load_github_repo_assignment.init_vectorstore()

    while True:
        query_type = user_list(
            "Select the type of query",
            ["understand_codebase", "feature_implementation"],
        )

        if query_type == "understand_codebase":
            await understand_codebase(load_github_repo_assignment)
        elif query_type == "feature_implementation":
            await feature_implementation(load_github_repo_assignment)
