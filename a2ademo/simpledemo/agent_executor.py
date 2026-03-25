
from .agent import GreetingAgent
from a2a.server.agent_execution import AgentExecutor
from a2a.server.events.event_queue import EventQueue
from a2a.server.agent_execution.context import RequestContext

class GreetingAgentExecutor(AgentExecutor):
    """A simple agent executor that runs the GreetingAgent."""

    def __init__(self):
        self.agent = GreetingAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        result = await self.agent.invoke()
        event_queue.enqueue_event({"type": "message", "data": result})

    
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise Exception("This agent cannot be cancelled.")

   