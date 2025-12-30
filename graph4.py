from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import Field, BaseModel
from typing import Literal

class ReviewState(BaseModel):
    review: str= Field(default=None, description="The generated review for the product.")
    rating: int= Field(default=None, description="The rating of the product out of 5.")
    rate_by: str= Field(default=None, description="The person who rated the product.")
    sentiment: Literal["Positive", "Negative"]= Field(default=None, description="The sentiment of the review.")

class ReviewOutput(BaseModel):
    sentiment: Literal["Positive", "Negative"]= Field(default=None, description="The sentiment of the review.")

load_dotenv()

llm = init_chat_model("gpt-3.5-turbo")

def find_sentiment(state: ReviewState):
    structured_llm = llm.with_structured_output(ReviewOutput)
    response = structured_llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that analyzes product reviews."},
        {"role": "user", "content": f"Analyze the following review and determine if it's Positive or Negative: {state.review}"}
    ])
    print("Sentiment Analysis Response:", response.sentiment)
    return {"sentiment": response.sentiment}

def negative_action(state: ReviewState):
    print("Performing negative action")
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that improves negative product reviews."},
        {"role": "user", "content": f"Improve the following negative review to make it more positive: {state.review}"}
    ])
    print("Negative Action Response:", response.content)
    return {"review": response.content}

def positive_action(state: ReviewState):
    print("Performing positive action")
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that enhances positive product reviews."},
        {"role": "user", "content": f"Enhance the following positive review to make it more engaging: {state.review}"}
    ])
    print("Positive Action Response:", response.content)
    return {"review": response.content}

def check_sentiment(state: ReviewState):

    print("Checking sentiment:", state.sentiment)
    if state.sentiment == "Negative":
        print("Routing to negative action")
        return {"negative": "negative_action"}
    else:
        print("Routing to positive action")
        return {"positive": "positive_action"}
        



workflow = StateGraph(ReviewState)

#adding nodes
workflow.add_node(find_sentiment)
workflow.add_node(negative_action)
workflow.add_node(positive_action)
workflow.add_node(check_sentiment)

#adding edges
workflow.add_edge(START, "find_sentiment")
workflow.add_edge("find_sentiment", "check_sentiment")
workflow.add_conditional_edges("check_sentiment", check_sentiment)
workflow.add_edge("negative_action", END)
workflow.add_edge("positive_action", END)

workflow = workflow.compile()

result = workflow.invoke({"review": "The product stopped working after a week. Very disappointed!"})

print(result)
print(workflow.get_graph().draw_ascii())
