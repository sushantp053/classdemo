from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
)

# Create an assistant agent with the model client
assistant_agent = AssistantAgent(name="assistant", model_client=model_client)


async def main() -> None:
    await Console(assistant_agent.run_stream(task="What is the capital of France?"))
    # Close the connection to the model client.
    await model_client.close()


# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
asyncio.run(main())