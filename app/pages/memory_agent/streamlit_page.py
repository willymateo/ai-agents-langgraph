import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.agents.AIModelSingleton import AIModelSingleton
from app.agents.constants.prompts import GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT
from app.pages.base_agent_chat import AgentChatWithMemoryPage
from app.pages.memory_agent.graph import build_graph


class MemoryAgentStreamlitPage(AgentChatWithMemoryPage):
    def __init__(self):
        super().__init__(
            title="AI Agent with Memory",
            name="ai_agent_with_memory",
            graph=self.get_graph(),
            description="This agent can remember previous interactions and use them to provide better responses.",
            system_message=GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT,
        )

    def get_graph(self) -> CompiledGraph:
        model = AIModelSingleton(model=st.session_state.ai_model_id)

        return build_graph(model)


if "memory_agent_instance" not in st.session_state:
    st.session_state.memory_agent_instance = MemoryAgentStreamlitPage()

st.session_state.memory_agent_instance.run()
