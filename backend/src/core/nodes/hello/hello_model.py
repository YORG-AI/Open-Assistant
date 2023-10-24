from pydantic import BaseModel


class HelloWorldInput(BaseModel):
    pass


class HelloWithNameInput(BaseModel):
    name: str
