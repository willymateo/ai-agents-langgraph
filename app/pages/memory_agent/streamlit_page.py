import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.graph import CompiledGraph

from app.agents.AIModelSingleton import AIModelSingleton
from app.agents.constants.prompts import GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT
from app.agents.utils.streaming import astream_langgraph_messages
from app.pages.base_ai_agent_chat import BaseAIAgentChat
from app.pages.memory_agent.graph import build_graph


class MemoryAgentStreamlitPage(BaseAIAgentChat):
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

    def on_user_input(self, user_input):
        st.session_state[f"{self.name}_user_input_is_enabled"] = False
        st.session_state[f"{self.name}_messages"].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        graph_config = RunnableConfig(configurable={"thread_id": "1234"})
        graph_state = self.graph.get_state(graph_config)
        input_messages = [HumanMessage(user_input)]

        if not graph_state.values.get("messages", []) and self.system_message:
            input_messages = [
                SystemMessage(self.system_message),
                HumanMessage(user_input),
            ]

        stream_response = self.graph.astream(
            input={"messages": input_messages},
            config=graph_config,
            stream_mode="messages",
        )

        with st.chat_message("assistant"):
            response = st.write_stream(astream_langgraph_messages(stream_response))
            st.session_state[f"{self.name}_user_input_is_enabled"] = True

        st.session_state[f"{self.name}_messages"].append(
            {
                "content": response,
                "role": "assistant",
            }
        )


if "memory_agent_instance" not in st.session_state:
    st.session_state.memory_agent_instance = MemoryAgentStreamlitPage()

st.session_state.memory_agent_instance.run()
