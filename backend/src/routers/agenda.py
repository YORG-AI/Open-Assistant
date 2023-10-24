from fastapi import APIRouter
# from src.core.user_input import UserInput
from pydantic import BaseModel

# from src.core.nodes.Hello.Hello import HelloNode
# from src.core.nodes.Hello.HelloModel import HelloWorldInput, HelloWithNameInput
# from src.core.nodes.LangChain.LangChainModel import LangChainInput
# from src.core.nodes.Anthropic.Anthropic import AnthropicNode, AnthropicModels
# from src.core.nodes.OpenAI.OpenAI import OpenAINode, OpenAIModels

# router = APIRouter(prefix="/agenda")


# class TestInput(BaseModel):
#     user_id: str
#     session_id: str
#     requirement: str


# @router.post(
#     "/create_agenda",
#     responses={403: {"description": "agenda creation not available at this time"}},
# )
# async def run(input: TestInput):
#     user_input = UserInput()
#     user_input.start_project(input.user_id, input.session_id, input.requirement)
#     return user_input
