import uvicorn
from starlette.applications import Starlette

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill
)

from .agent_executor import GreetingAgentExecutor

if __name__ == "__main__":
    
    skill = AgentSkill(
        id="greeting_skill",
        name="Greeting Skill",
        description="A skill that greets the user.",
        tags=["greeting", "simple"],
        examples=[
            "Hello, how are you?",
            "Hi there!"
        ]

    )

    agentCard = AgentCard(
        id="greeting_agent",
        name="Greeting Agent",
        description="A simple agent that greets the user.",
        tags=["greeting", "simple"],
        url="http://localhost:9999/",
        version="1.0.0",
        skills=[skill],
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities()
    )

    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agentCard,
        http_handler=request_handler,
    )

    app = Starlette(routes=server.routes())

    uvicorn.run(app, host="0.0.0.0", port=9999)
