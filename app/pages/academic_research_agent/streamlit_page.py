import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.agents.AIModelSingleton import AIModelSingleton
from app.pages.academic_research_agent.constants import (
    ACADEMIC_RESEARCHER_SYSTEM_PROMPT,
)
from app.pages.academic_research_agent.graph import build_graph
from app.pages.base_agent_chat import AgentChatWithMemoryPage


class AcademicResearchAgentStreamlitPage(AgentChatWithMemoryPage):
    def __init__(self):
        super().__init__(
            title="Academic Research Agent",
            name="academic_research_agent",
            graph=self.get_graph(),
            description="This agent can answer questions based on the provided research paper.",
            system_message=ACADEMIC_RESEARCHER_SYSTEM_PROMPT,
        )

    def get_graph(self) -> CompiledGraph:
        model = AIModelSingleton(model=st.session_state.ai_model_id)

        return build_graph(model)

    def display_page_content(self):
        st.title(self.title)

        if self.description:
            st.info(self.description, icon="ℹ️")

        uploaded_file = st.file_uploader(
            "Upload a research paper",
            help="Upload a PDF file containing the research paper you want to analyze.",
            accept_multiple_files=False,
            type=["pdf"],
        )

        for message in self.get_session_state_value("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input_is_enabled = self.get_session_state_value(
            "user_input_is_enabled", False
        )

        user_input = st.chat_input(
            "What do you want to ask the AI?", disabled=not user_input_is_enabled
        )

        if user_input:
            self.on_user_input(user_input)


if "academic_research_agent_instance" not in st.session_state:
    st.session_state.academic_research_agent_instance = (
        AcademicResearchAgentStreamlitPage()
    )

st.session_state.academic_research_agent_instance.run()
