from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field
from langchain.chat_models import init_chat_model
from typing import Literal

class TwitterState(BaseModel):
    topic: str = Field(default="", description="Topic of the tweet")
    tweet_lenght: int = Field(default=280, description="Length of the tweet")
    sentiment: str = Field(default="", description="Sentiment of the tweet")
    evolution: int = Field(default=0, description="Evolution of the tweet sentiment")
    tone: str = Field(default="", description="Tone of the tweet")
    tweet: str = Field(default="", description="Generated tweet")
    max_evolution: int = Field(default=5, description="Maximum evolution steps")

class TweeSentiment(BaseModel):
    accept: Literal["accepted", "need improvement"] = Field(default="need improvement", description="Whether the tweet is accepted or not")


load_dotenv()

llm = init_chat_model("gpt-3.5-turbo", temperature=0.7)

def genrate_tweet(state: TwitterState):
    # Placeholder for tweet generation logic
    prompt = f"""You are Twitter inflencer where you create tweet based upon 
    following topic {state.topic}
    Tweet should be of maximum length {state.tweet_lenght} characters. 
    Tweet does not contain Question answer types
    Tweet should have a tone of {state.tone}.
    Tweet should have a attractive and engaging content.
    Tweet should not contain any hashtags."""

    tweet_content = llm.invoke(prompt)
    return {"tweet": tweet_content.content}

def anylze_sentiment(state: TwitterState):
    
    prompt = f"""You are a sentiment analysis expert and trained anylist where you analyze tone.
    Analyze the sentiment of the following tweet: {state.tweet}
    Provide the accepted, need improvement depend upon following criteria 
    If the tweet is positive and engaging then it is accepted 
    Tweet lenght should be less than {state.tweet_lenght} characters.
    Tone of the tweet should be {state.tone}. 
    Tweet should not contain any hashtags. 
    Tweet should have attractive and engaging content. 
    If any of the criteria is not met then it need improvement."""
    
    structured_llm = llm.with_structured_output(TweeSentiment)
    result = structured_llm.invoke(prompt)
    return {"sentiment": result.accept}

def evolve_tweet(state: TwitterState):
    # Placeholder for sentiment evolution logic
    prompt = f"""You are Twitter inflencer where evolve the following tweet {state.tweet}
    Tweet should be of maximum length {state.tweet_lenght} characters. 
    Tweet does not contain Question answer types
    Tweet should have a tone of {state.tone}.
    Tweet should have a attractive and engaging content.
    Tweet should not contain any hashtags."""
    tweet_content = llm.invoke(prompt)
    return {"tweet": tweet_content.content, "evolution": state.evolution + 1}

def check_acceptance(state: TwitterState):
    if state.sentiment == "need improvement" and state.evolution < state.max_evolution:
        print("Routing to negative action")
        return "negative"
    else:
        print("Routing to positive action")
        return "positive"
    
def optimize_tweet(state: TwitterState) -> TwitterState:
    print("Final optimized tweet:", state.tweet)
    prompt = f"""You are Twitter inflencer where you optimize the following tweet {state.tweet} with proper hashtags."""
    
    tweet_content = llm.invoke(prompt)
    return {"tweet": tweet_content.content}
        
def genTweet(topic: str, tweet_lenght: int, tone: str, max_evolution: int):
    graph = StateGraph(TwitterState)

    #adding nodes
    graph.add_node("genrate_tweet", genrate_tweet)
    graph.add_node("anylze_sentiment", anylze_sentiment)
    graph.add_node("evolve_tweet", evolve_tweet)
    graph.add_node("optimize_tweet", optimize_tweet)

    #adding edges
    graph.add_edge(START, "genrate_tweet")
    graph.add_edge("genrate_tweet", "anylze_sentiment")
    graph.add_conditional_edges(
    "anylze_sentiment", 
    check_acceptance, 
    {"negative": "evolve_tweet", "positive": "optimize_tweet"}
    )
    graph.add_edge("evolve_tweet", "anylze_sentiment")
    graph.add_edge("optimize_tweet", END)

    graph = graph.compile()
    result = graph.invoke({"topic": topic, "tweet_lenght": tweet_lenght, "tone": tone, "max_evolution": max_evolution})
    return result


def __main__():
    genTweet("Artificial Intelligence", 140, "Humorous", 3)