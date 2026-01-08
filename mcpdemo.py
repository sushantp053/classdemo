from fastmcp import FastMCP

mcp = FastMCP("stock")

@mcp.tool
def get_stock_price(ticker: str) -> float:
    """Get the current stock price for the given ticker symbol."""
    # Mock implementation, replace with actual API call
    stock_prices = {"AAPL": 155.30, "GOOGL": 2735.45, "MSFT": 299.35}
    return stock_prices.get(ticker.upper(), 0.0)

@mcp.tool
def purchase_stock(ticker: str, quantity: int) -> str:
    """Purchase a specified quantity of stock for the given ticker symbol."""
    # Mock implementation, replace with actual purchase logic
    return f"Purchased {quantity} shares of {ticker}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
