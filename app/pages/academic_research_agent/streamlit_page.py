from typing import Any

import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.agents.AIModelSingleton import AIModelSingleton
from app.pages.academic_research_agent.graph import build_graph


class AcademicResearchAgentStreamlitPage:
    def __init__(self):
        self.graph_model = st.session_state.ai_model_id
        self.graph = self.get_graph()
        self.name = "academic_research_agent"

        self.initialize_session_state()

    def initialize_session_state(self):
        messages = self.get_session_state_value("messages")

        if messages is None:
            self.set_session_state_value("messages", [])

    def get_graph(self) -> CompiledGraph:
        model = AIModelSingleton(model=st.session_state.ai_model_id)

        return build_graph(model)

    def get_session_state_value(self, parameter_name: str, default_value: Any = None):
        return st.session_state.get(f"{self.name}_{parameter_name}", default_value)

    def set_session_state_value(self, parameter_name: str, value: Any):
        st.session_state[f"{self.name}_{parameter_name}"] = value

    def display_page_content(self):
        st.title("Podcast Agent")

        st.info(
            "This agent can create a podcast script based on a topic and news articles.",
            icon="ℹ️",
        )

        for message in self.get_session_state_value("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def run(self):
        if self.graph_model != st.session_state.ai_model_id:
            self.graph_model = st.session_state.ai_model_id
            self.graph = self.get_graph()

        self.display_page_content()


if "academic_research_agent_instance" not in st.session_state:
    st.session_state.academic_research_agent_instance = (
        AcademicResearchAgentStreamlitPage()
    )

st.session_state.academic_research_agent_instance.run()
