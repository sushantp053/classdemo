from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

def llm_research(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "As per my research, the information is accurate."}]}

graph = StateGraph(MessagesState)

####### Add nodes and edges to the graph
graph.add_node(mock_llm)
graph.add_node(llm_research)

######## Adding edges
graph.add_edge(START, "mock_llm")
graph.add_edge(START, "llm_research")
graph.add_edge("mock_llm", "llm_research")
graph.add_edge("mock_llm", END)
graph.add_edge("llm_research", END)

##### Compile and invoke the graph
graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

print(result)

print(graph.get_graph().draw_ascii())