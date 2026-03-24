from fastmcp import FastMCP
from pydantic import Field, BaseModel

mcp = FastMCP("my todo manager")

class TodoItem(BaseModel):
    title: str
    description: str
    id: int = Field(default_factory=int)
    status: str = Field(default="pending")

list_of_todos = []

@mcp.tool
def add_todo_item(title: str, description: str) -> str:
    """Add a new item to the todo list. Requires title and description."""
    # Mock implementation, replace with actual storage logic
    new_item = TodoItem(title=title, description=description, id=len(list_of_todos) + 1)
    list_of_todos.append(new_item)

    return f"Added todo item: {title}"

@mcp.tool
def get_todo_items() -> list[TodoItem]:
    """Retrieve all todo items."""
    # Mock implementation, replace with actual retrieval logic
    return list_of_todos

@mcp.resource("todo://all")
def get_all_todo_items() -> list[TodoItem]:
    """Retrieve all todo items."""
    # Mock implementation, replace with actual retrieval logic
    return list_of_todos

@mcp.tool
def mark_todo_item_completed(item_id: int) -> str:
    """Mark a todo item as completed."""
    # Mock implementation, replace with actual update logic
    for item in list_of_todos:
        if item.id == item_id:
            item.status = "completed"
    return f"Marked todo item {item_id} as completed"

@mcp.resource("todo://{id}")
def get_todo_item(id: int) -> TodoItem:
    """Retrieve a specific todo item by ID."""
    # Mock implementation, replace with actual retrieval logic
    for item in list_of_todos:
        if item.id == id:
            return item
    return None

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)