from typing import Optional
from enum import Enum
from markdown import markdown
from ipykernel.kernelbase import Kernel
from ipywidgets import widgets

from .handler import Handler, HandlerInput

from src.core.agents.software_engineer.software_engineer import (
    SoftwareEngineerAgent,
    Plan,
)


class Stage(str, Enum):
    INIT = "init"
    WAIT_FOR_GIT_REPO = "wait_for_git_repo"
    SET_GIT_REPO_DONE = "set_git_repo_done"
    WAIT_FOR_FEATURE = "wait_for_feature"
    SET_FEATURE_DONE = "set_feature_done"
    MODIFY_FOCUS_FILES = "modify_focus_files"
    WAIT_FOR_MODIFY_FOCUS_FILES = "wait_for_modify_focus_files"
    MODIFY_FOCUS_FILES_DONE = "modify_focus_files_done"
    MODIFY_PLAN = "modify_plan"
    WAIT_FOR_MODIFY_PLAN = "wait_for_modify_plan"
    GENERATE_ACTION = "generate_action"
    APPLY_ACTION = "apply_action"
    WAIT_APPLY_ACTION = "wait_apply_action"
    DONE = "done"


def _auto_retry(retry_stage: Stage):
    """
    Auto retry function.
    """

    def decorator(func: callable):
        def wrapper(self):
            try:
                func(self)
            except Exception as e:
                self._send_markdown("Error occurred: " + str(e))

                retry_botton = widgets.Button(
                    value=False,
                    description="Retry",
                    disabled=False,
                    button_style="",  # 'success', 'info', 'warning', 'danger' or ''
                    tooltip="Description",
                    icon="redo",  # (FontAwesome names without the `fa-` prefix)
                )

                def retry_button_clicked(b):
                    retry_botton.disabled = True
                    self._next()

                retry_botton.on_click(retry_button_clicked)

                self._send_widget(retry_botton)
                self.current_stage = retry_stage

        return wrapper

    return decorator


class StatefulAgent:
    def __init__(self, agent: SoftwareEngineerAgent, handler: Handler):
        self.agent = agent
        self.current_stage = Stage.INIT
        self.step_cnt = 1
        self.handler = handler

    def next(self):
        self._send_markdown("### step " + str(self.step_cnt) + ":" + "\n\n---")
        self.step_cnt += 1
        match self.current_stage:
            case Stage.INIT:
                self._on_init()
            case Stage.SET_GIT_REPO_DONE:
                self._on_set_git_repo_done()
            case Stage.SET_FEATURE_DONE:
                self._on_set_feature_done()
            case Stage.MODIFY_FOCUS_FILES:
                self._on_modify_focus_files()
            case Stage.MODIFY_FOCUS_FILES_DONE:
                self._on_modify_focus_files_done()
            case Stage.MODIFY_PLAN:
                self._on_modify_plan()
            case Stage.GENERATE_ACTION:
                self._on_generate_action()
            case Stage.APPLY_ACTION:
                self._on_apply_action()
            case Stage.DONE:
                self._send_markdown("Task done.")

    @_auto_retry(Stage.INIT)
    def _on_init(self):
        self._send_markdown(
            "> Please provide the repo url or name of the repo under `src/data/git`"
        )
        repo_text = widgets.Text(
            value="http://www.github.com/xxx/xxx",
            placeholder="Type something",
            description="URL: ",
            disabled=False,
        )
        next_button = widgets.Button(
            value=False,
            description="Next",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )

        def next_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_GIT_REPO:
                repo_url = repo_text.value
                if repo_url.startswith("http"):
                    self.agent.set_repo_url(repo_url)
                else:
                    self.agent.set_local_repo(repo_url)
                self.current_stage = Stage.SET_GIT_REPO_DONE
                self.next()

        vbox = widgets.VBox([repo_text, next_button])
        next_button.on_click(next_button_clicked)
        self._send_widget(vbox)

        self.current_stage = Stage.WAIT_FOR_GIT_REPO

    @_auto_retry(Stage.SET_GIT_REPO_DONE)
    def _on_set_git_repo_done(self):
        self._send_markdown("> Please provide the feature")
        feature_text = widgets.Text(
            value="Hello World",
            placeholder="Type something",
            description="Feature:",
            disabled=False,
        )
        next_bottom = widgets.Button(
            value=False,
            description="Next",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )

        def next_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_FEATURE:
                feature = feature_text.value
                self.agent.set_feature_description(feature)
                self.current_stage = Stage.SET_FEATURE_DONE
                self.next()

        vbox = widgets.VBox([feature_text, next_bottom])
        next_bottom.on_click(next_button_clicked)
        self._send_widget(vbox)
        self.current_stage = Stage.WAIT_FOR_FEATURE

    @_auto_retry(Stage.SET_FEATURE_DONE)
    def _on_set_feature_done(self):
        try:
            self._send_markdown("> LLM is picking focus files...")
            self.agent.set_focus_files()

            focus_files = list(self.agent.get_focus_files())
            focus_files_msg = "LLM think the files that are relative to the feature implementation are as follows:"
            for path in focus_files:
                focus_files_msg += "\n\n - " + path

            self._send_markdown(focus_files_msg)
            self.current_stage = Stage.MODIFY_FOCUS_FILES
            self.next()
        except Exception as e:
            self._send_markdown("Error occurred: " + str(e))

            self.current_stage = Stage.SET_FEATURE_DONE
            self.next()

    @_auto_retry(Stage.MODIFY_FOCUS_FILES)
    def _on_modify_focus_files(self):
        self._send_markdown("> You can Edit the focus files if you want.")

        focus_files = list(self.agent.get_focus_files())

        box = widgets.VBox()

        def add_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_FOCUS_FILES:
                focus_files.append("")
                update_list()

        def on_text_change(change, idx):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_FOCUS_FILES:
                focus_files[idx] = change.new

        def remove_button_clicked(b, idx):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_FOCUS_FILES:
                focus_files.pop(idx)
                update_list()

        def update_list():
            # create text and remove buttom for each focus file
            items = [
                widgets.HBox(
                    [
                        widgets.Text(
                            value=focus_file,
                            placeholder="Focus file path",
                            description=f"{idx}:",
                            disabled=False,
                            layout=widgets.Layout(width="75%"),
                        ),
                        widgets.Button(
                            value=False,
                            description="",
                            disabled=False,
                            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
                            tooltip="Remove this focus file",
                            icon="trash",  # (FontAwesome names without the `fa-` prefix)
                            layout=widgets.Layout(height="22pt", width="22pt"),
                        ),
                    ]
                )
                for idx, focus_file in enumerate(focus_files)
            ]
            for idx, item in enumerate(items):
                item.children[0].observe(
                    lambda change, idx=idx: on_text_change(change, idx), names="value"
                )
                item.children[1].on_click(
                    lambda b, idx=idx: remove_button_clicked(b, idx)
                )

            box.children = items

        # add file button
        add_button = widgets.Button(
            value=False,
            description="Add",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="plus",  # (FontAwesome names without the `fa-` prefix)
        )

        add_button.on_click(add_button_clicked)

        # next button
        next_button = widgets.Button(
            value=False,
            description="Next",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )

        def next_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_FOCUS_FILES:
                for focus_file in focus_files:
                    self.agent.add_focus_file(focus_file)
                self.current_stage = Stage.MODIFY_FOCUS_FILES_DONE

                self.next()

        next_button.on_click(next_button_clicked)

        update_list()

        self._send_widget(box)
        self._send_widget(add_button)
        self._send_widget(next_button)

        self.current_stage = Stage.WAIT_FOR_MODIFY_FOCUS_FILES

    @_auto_retry(Stage.MODIFY_FOCUS_FILES_DONE)
    def _on_modify_focus_files_done(self):
        self._send_markdown("> LLM is planning the implementation...")
        self.agent.design_plan()

        plans = self.agent.get_plan()
        plan_msg = "LLM think the implementation plan is as follows:"
        for plan in plans:
            plan_msg += "\n" + plan.to_markdown() + "\n"

        self._send_markdown(plan_msg)
        self.current_stage = Stage.MODIFY_PLAN
        self.next()

    @_auto_retry(Stage.MODIFY_PLAN)
    def _on_modify_plan(self):
        plans = self.agent.get_plan()

        box = widgets.VBox()

        def on_action_change(change, idx: int):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                if change.new == "add":
                    plans[idx].action = "add"
                elif change.new == "remove":
                    plans[idx].action = "remove"
                elif change.new == "modify":
                    plans[idx].action = "modify"

        def on_file_path_change(change, idx: int):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                plans[idx].file_path = change.new

        def on_description_change(change, idx: int):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                plans[idx].description = change.new

        def remove_button_clicked(b, idx: int):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                plans.pop(idx)
                update_list()

        def update_list():
            # create text and remove buttom for each plan
            items = [
                widgets.VBox(
                    [
                        widgets.Label(value=f"Plan #{idx}:"),
                        widgets.Dropdown(
                            options=["add", "remove", "modify"],
                            value=plan.action,
                            description="Action:",
                            disabled=False,
                        ),
                        widgets.Text(
                            value=plan.file_path,
                            placeholder="File path",
                            description="File path:",
                            disabled=False,
                            layout=widgets.Layout(width="75%"),
                        ),
                        widgets.Textarea(
                            value=plan.description,
                            placeholder="Description",
                            description="Description:",
                            disabled=False,
                            layout=widgets.Layout(width="75%"),
                        ),
                        widgets.Button(
                            value=False,
                            description="",
                            disabled=False,
                            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
                            tooltip="Remove this plan",
                            icon="trash",  # (FontAwesome names without the `fa-` prefix)
                            layout=widgets.Layout(height="22pt", width="22pt"),
                        ),
                    ]
                )
                for idx, plan in enumerate(plans)
            ]

            for idx, item in enumerate(items):
                item.children[1].observe(
                    lambda change, idx=idx: on_action_change(change, idx), names="value"
                )
                item.children[2].observe(
                    lambda change, idx=idx: on_file_path_change(change, idx),
                    names="value",
                )
                item.children[3].observe(
                    lambda change, idx=idx: on_description_change(change, idx),
                    names="value",
                )
                item.children[4].on_click(
                    lambda b, idx=idx: remove_button_clicked(b, idx)
                )

            box.children = items

        add_button = widgets.Button(
            value=False,
            description="Add",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="plus",  # (FontAwesome names without the `fa-` prefix)
        )

        next_button = widgets.Button(
            value=False,
            description="Next",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )

        def add_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                plans.append(Plan(action="add", file_path="", description=""))
                update_list()

        def next_button_clicked(b):
            if self.current_stage == Stage.WAIT_FOR_MODIFY_PLAN:
                self.agent.set_plans(plans)
                self.current_stage = Stage.GENERATE_ACTION
                self.next()

        add_button.on_click(add_button_clicked)
        next_button.on_click(next_button_clicked)

        update_list()

        self._send_widget(box)
        self._send_widget(add_button)
        self._send_widget(next_button)

        self.current_stage = Stage.WAIT_FOR_MODIFY_PLAN

    @_auto_retry(Stage.GENERATE_ACTION)
    def _on_generate_action(self):
        self._send_markdown("> LLM is generating actions...")
        for action in self.agent.implement():
            self._send_markdown(f"{action}")

        self.current_stage = Stage.APPLY_ACTION
        self.next()

    @_auto_retry(Stage.APPLY_ACTION)
    def _on_apply_action(self):
        self._send_markdown("> Do you want to apply the actions?")

        yes_button = widgets.Button(
            description="Yes",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="check",  # (FontAwesome names without the `fa-` prefix)
        )

        no_button = widgets.Button(
            description="No",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Description",
            icon="times",  # (FontAwesome names without the `fa-` prefix)
        )

        def yes_button_clicked(b):
            if self.current_stage == Stage.WAIT_APPLY_ACTION:
                self.agent.apply_file_action()
                self._send_markdown("Actions applied.")
                self.current_stage = Stage.DONE
                self.next()

        def no_button_clicked(b):
            if self.current_stage == Stage.WAIT_APPLY_ACTION:
                self._send_markdown("Actions discarded.")
                self.current_stage = Stage.DONE
                self.next()

        yes_button.on_click(yes_button_clicked)
        no_button.on_click(no_button_clicked)

        box = widgets.HBox([yes_button, no_button])

        self._send_widget(box)
        self.current_stage = Stage.WAIT_APPLY_ACTION

    def _send_widget(self, widget: widgets.Widget):
        self.handler._send_widget(widget)

    def _send_markdown(self, content: str):
        self.handler._send_markdown(content)


class SoftwareEngineerAgentHandler(Handler):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

        self.agents: dict[str, StatefulAgent] = {}

    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        if input.cell_id is None:
            raise Exception("cell_id is None")

        if input.cell_id not in self.agents:
            self.agents[input.cell_id] = StatefulAgent(
                SoftwareEngineerAgent(), self
            )

        self.agents[input.cell_id].next()

    def do_shutdown(self, restart: bool):
        pass
