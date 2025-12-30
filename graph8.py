from langgraph.checkpoint.memory import InMemorySaver  
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict

class Context(TypedDict):
    message : str


def createMessage(state: Context):
    return {"message": f"Hello, {state['message']}!"}


checkpointer = InMemorySaver()


message_graph = StateGraph(Context)

# Add nodes and edges to the graph
message_graph.add_node(createMessage, name="createMessage")


# Adding edges
message_graph.add_edge(START, "createMessage")
message_graph.add_edge("createMessage", END)

graph = message_graph.compile(checkpointer=checkpointer)

response = graph.invoke({"message": "World"}, {"configurable": {"thread_id": "1"}})

print(response)

print(graph.get_state({"configurable": {"thread_id": "1"}}))


response = graph.invoke({"message": "my new message"}, {"configurable": {"thread_id": "2"}})

print(response)

print(graph.get_state({"configurable": {"thread_id": "1"}}))
print(graph.get_state({"configurable": {"thread_id": "2"}}))
