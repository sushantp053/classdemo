from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("stock")

@mcp.tool
async def get_stock_price(ticker: str) -> float:
    """Get the current stock price for the given ticker symbol."""
    # Mock implementation, replace with actual API call
    stock_prices = {"AAPL": 155.30, "GOOGL": 2735.45, "MSFT": 299.35}
    return stock_prices.get(ticker.upper(), 0.0)

@mcp.tool
async def purchase_stock(ticker: str, quantity: int) -> str:
    """Purchase a specified quantity of stock for the given ticker symbol."""
    # Mock implementation, replace with actual purchase logic
    return f"Purchased {quantity} shares of {ticker}"

@mcp.resource("resource://stock_portfolio")
def stock_portfolio() -> dict:
    """Return a stock portfolio."""
    return {
        "AAPL": 50,
        "GOOGL": 10,
        "MSFT": 20
    }

@mcp.prompt(name="stock_prompt", description="Prompt for stock trading assistant")
def stock_prompt() -> str:
    '''Provide a prompt for the stock trading assistant.'''
    return """You are a stock trading assistant. You can provide stock prices and help with purchasing stocks.
Use the tools available to assist users with their stock trading needs."""


@mcp.prompt(name="stock_analyst_prompt", description="Prompt for stock market analyst")
def stock_analyst_prompt(ticker: str = Field(description="Ticker symbol")) -> str:
    '''Provide a prompt for the stock market analyst.'''
    return f"""You are a stock market analyst. You analyze stock trends and provide insights of {ticker}.
Use the tools available to assist users with their stock market analysis needs."""

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # mcp.run(transport="stdio")
