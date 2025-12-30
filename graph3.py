from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import Field, BaseModel


class BlogState(BaseModel):
    topic: str= Field(..., description="The topic of the blog post.")
    outline: str= Field(default=None, description="The outline of the blog post.")
    final: str= Field(default=None, description="The final version of the blog post.")

load_dotenv()

llm = init_chat_model("gpt-3.5-turbo")

def generate_outline(state: BlogState):

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that generates blog outlines."},
        {"role": "user", "content": f"Generate an outline for a blog post on the topic: {state.topic}"}
    ])
    return {"outline": response.content}

def generate_final(state: BlogState):

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that writes blog posts."},
        {"role": "user", "content": f"Write a detailed blog post based on the following outline: {state.topic}"}
    ])
    return {"final": response.content}

def generate_output(state: BlogState):
    if state.outline and state.final:
        return BlogState(
        topic=state.topic,
        outline=state.outline,
        final=state.final
        )
    return state

graph = StateGraph(BlogState)
#adding nodes
graph.add_node(generate_outline)
graph.add_node(generate_final)
graph.add_node(generate_output)

#adding edges
graph.add_edge(START, "generate_outline")
graph.add_edge(START, "generate_final")
graph.add_edge("generate_outline", "generate_output")
graph.add_edge("generate_final", "generate_output")
graph.add_edge("generate_output", END)


graph = graph.compile()

result = graph.invoke({"topic": "The benefits of learning Python programming."})

print(result['final'])

print(result['outline'])

print(graph.get_graph().draw_ascii())
