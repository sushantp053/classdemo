from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()

client = MultiServerMCPClient(
    {
        "todo": {
            "transport": "http",
            "url": "http://0.0.0.0:8000/mcp",
        },
    }
)

async def callAgent():
    tools = await client.get_tools()
    print("Loaded tools:", tools)
    agent = create_agent("openai:gpt-4.1", tools)
    # response = await agent.ainvoke({"messages": "Mark My Buy Grocery has completed. What are my todo items?"})
    # print(response)

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = await agent.ainvoke({"messages": user_input})
        print("Agent:", response)

# async.run(callAgent())

if __name__ == "__main__":
    import asyncio
    asyncio.run(callAgent())