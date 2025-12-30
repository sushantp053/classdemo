from fastapi import FastAPI
import graph6 as g
from pydantic import BaseModel

app = FastAPI()

class TweetRequest(BaseModel):
    topic: str
    tweet_length: int
    tone: str
    max_evolution: int


@app.post("/generate")
def generate_tweet(request: TweetRequest):
    tweet = g.genTweet(request.topic, request.tweet_length, request.tone, request.max_evolution)
    return {"tweet": tweet['tweet']}