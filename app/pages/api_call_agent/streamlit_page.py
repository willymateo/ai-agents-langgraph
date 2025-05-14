from app.agents.constants.prompts import GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT
from app.pages.api_call_agent.graph import graph
from app.pages.base_ai_agent_chat import BaseAIAgentChat

api_call_agent = BaseAIAgentChat(
    title="API Call Agent",
    name="api_call_agent",
    graph=graph,
    description="This agent can call APIs to get information.",
    system_message=GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT,
)

api_call_agent.run()
