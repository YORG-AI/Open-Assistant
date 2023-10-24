from fastapi import APIRouter, FastAPI, UploadFile
from typing import Type
from ..app import app
from .singleton import Singleton

def node_router_post(router, cls, func_name, func):
    if "properties" in func.__annotations__:
        if func.__defaults__ is not None and len(func.__defaults__) == 2:

            @router.post(
                f"/{func_name}",
                responses={
                    403: {"description": f"{func_name} is not available at this time"}
                },
            )
            async def run(
                input: func.__annotations__["input"] = func.__defaults__[0],
                properties: func.__annotations__["properties"] = func.__defaults__[1],
            ):
                node = cls()
                return func(node, input, properties)

        elif func.__defaults__ is not None and len(func.__defaults__) == 1:

            @router.post(
                f"/{func_name}",
                responses={
                    403: {"description": f"{func_name} is not available at this time"}
                },
            )
            async def run(
                properties: func.__annotations__["properties"],
                input: func.__annotations__["input"] = func.__defaults__[0],
            ):
                node = cls()
                return func(node, input, properties)

        else:

            @router.post(
                f"/{func_name}",
                responses={
                    403: {"description": f"{func_name} is not available at this time"}
                },
            )
            async def run(
                input: func.__annotations__["input"],
                properties: func.__annotations__["properties"],
            ):
                node = cls()
                return func(node, input, properties)

    else:
        if func.__defaults__ is not None:

            @router.post(
                f"/{func_name}",
                responses={
                    403: {"description": f"{func_name} is not available at this time"}
                },
            )
            async def run(input: func.__annotations__["input"] = func.__defaults__[0]):
                node = cls()
                return func(node, input)

        else:

            @router.post(
                f"/{func_name}",
                responses={
                    403: {"description": f"{func_name} is not available at this time"}
                },
            )
            async def run(input: func.__annotations__["input"]):
                node = cls()
                return func(node, input)


def generate_node_end_points(cls):
    router = APIRouter(prefix=f"/nodes/{cls.config.name}")
    for func_name in cls.config.functions.keys():
        if not hasattr(cls, func_name):
            raise Exception(
                f"Cannot generate end point for node {cls.config.name}: Function {func_name} not exist."
            )
        else:
            node_router_post(router, cls, func_name, getattr(cls, func_name))
    app.include_router(router)
    return cls


def generate_assignment_end_point(cls):
    assignment = cls()
    if not hasattr(assignment, "run"):
        raise Exception(
            f"Cannot generate end point for assignment {assignment.config.name}: Function run not exist."
        )
    else:
        router = APIRouter(prefix=f"/assignments/{assignment.config.name}")
        @router.post(
            f"/run",
            responses={
                403: {"description": f"{assignment.config.name} is not available at this time"}
            },
        )
        async def run(input: assignment.run.__annotations__["input"]):
            output = await assignment.run(input)
            output.load(output.raw_output)
            return output.formatted_output

    app.include_router(router)
    return cls
