from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field

from langchain.chat_models import init_chat_model
import requests

url = "https://api.kie.ai/api/v1/veo/generate"

load_dotenv()

llm = init_chat_model("gpt-3.5-turbo", temperature=0.5)

class VideoState(BaseModel):
    topic: str = Field(default="", description="Topic of the video")
    content: str = Field(default="", description="Content of the video")
    video_length: int = Field(default=10, description="Length of the video in seconds")
    tone: str = Field(default="", description="Tone of the video")
    script: str = Field(default="", description="Generated video script")
    scenes: str = Field(default="", description="Generated video scenes")
    oririentation: str = Field(default="landscape", description="Orientation of the video")
    gen_response: str = Field(default="", description="Response from video generation API")
    url: str = Field(default="", description="Generated video URL")

def topicWebSearch(state: VideoState):
    prompt = f"""You are a web search expert where you search the web for latest information 
    about following topic {state.topic}
    Provide only relevant information without any additional text."""

    info = llm.invoke(prompt)
    return {"topic_info": info.content}


def contentGeneration(state: VideoState):
    prompt = f"""You are a video content creator where you create video content based upon 
    following topic {state.topic}
    Video should be of maximum length {state.video_length} seconds. 
    Video should have a tone of {state.tone}.
    Video should have attractive and engaging content.
    Video should be in {state.oririentation} orientation.
    Provide only content without any additional text."""

    content = llm.invoke(prompt)
    return {"content": content.content}

def scriptGeneration(state: VideoState):
    prompt = f"""You are a video script writer where you create video script based upon 
    following content {state.content}
    Video should be of maximum length {state.video_length} seconds. 
    Video should have a tone of {state.tone}.
    Video should have attractive and engaging content.
    Video should be in {state.oririentation} orientation.
    Provide only script without any additional text."""

    script = llm.invoke(prompt)
    return {"script": script.content}

def videoGeneration(state: VideoState):
    payload = {
    "prompt": f"{state.script}",
    "model": "veo3_fast",
    "aspectRatio": "16:9",
    "enableFallback": False,
    "enableTranslation": True,
    "generationType": "TEXT_2_VIDEO"
    }
    headers = {
        "Authorization": "Bearer 54a267134ec0b6225086032e4e11ee5b",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    
    return {"gen_response": response.text}
    

graph = StateGraph(VideoState)

#adding nodes
graph.add_node(contentGeneration)
graph.add_node(scriptGeneration)
graph.add_node(videoGeneration)

#adding edges
graph.add_edge(START, "contentGeneration")
graph.add_edge("contentGeneration", "scriptGeneration")
graph.add_edge("scriptGeneration", "videoGeneration")
graph.add_edge("videoGeneration", END)

graph = graph.compile()

result = graph.invoke({"topic": "Langgraph and langchain differnce", "video_length": 10, "tone": "informative", "oririentation": "landscape"})

print(result['script'])
print(result['content'])
print(result['gen_response'])

