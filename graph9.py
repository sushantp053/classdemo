from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver 
from langchain.tools import tool
from dotenv import load_dotenv
from langgraph.types import Command

load_dotenv()


@tool
def get_stock_price(ticker: str) -> str:
    """Fetch the current stock price for the given ticker symbol."""
    price = 123.45  # Placeholder for actual stock price fetching logic
    return f"The current price of {ticker} is ${price}"

@tool
def purchase_stock(ticker: str, quantity: int) -> str:
    """Purchase a specified quantity of stock for the given ticker symbol."""
    return f"Purchased {quantity} shares of {ticker}"


checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-3.5-turbo",
    tools=[get_stock_price, purchase_stock],
    checkpointer=checkpointer,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "purchase_stock": {
                    "allowed_decisions": ["approve", "reject"],
                    "description": "Do you want to purchase the stock?",
                }
            },
        )
    ],
)

config = {"configurable": {"thread_id": "1"}} 

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current price of AAPL stock and buy 10 shares if the price is below $150?",
            }
        ]
    },
    config = config,
)

print(response)

for message in response["messages"]:
    message.pretty_print()


resp = agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}  # or "reject"
    ), 
    config=config,
)

print(resp)

for message in resp["messages"]:
    message.pretty_print()


r = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current price of AAPL stock and buy 10 shares   if the price is below $150?",
            }
        ]       
    },
    config={"configurable": {"thread_id": "2"}},
)


print(r)

for message in r["messages"]:
    message.pretty_print()