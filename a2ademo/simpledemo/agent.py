import uuid

from langchain.agents import create_agent
from pydantic import BaseModel

from a2a.types import Message, Part, Role, TextPart


class GreetingAgent(BaseModel):
    """A simple agent that greets the user."""

    async def invoke(self) -> str:
        # agent = create_agent(
        #     model="gpt-3.5-turbo",
        # )
        return "Hello! Kay chalaly agent banavayala chalu kara ?"