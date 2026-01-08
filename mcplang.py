from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()

client = MultiServerMCPClient(
    {
        # "stock": {
        #     "transport": "http",
        #     "url": "http://localhost:8000/stock",
        # }
        "stock": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["mcpdemo.py"],
        }
    }
)

async def callAgent():
    tools = await client.get_tools()
    agent = create_agent("openai:gpt-4.1", tools)
    response = await agent.ainvoke({"messages": "what is the stock price of AAPL? Buy 10 shares if the price is below $150."})
    print(response)

    for message in response["messages"]:
        message.pretty_print()

# async.run(callAgent())

if __name__ == "__main__":
    import asyncio
    asyncio.run(callAgent())