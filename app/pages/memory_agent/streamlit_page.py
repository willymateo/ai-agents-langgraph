import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig

from app.agents.constants.prompts import GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT
from app.agents.utils.streaming import stream_langgraph_messages
from app.pages.base_ai_agent_chat import BaseAIAgentChat
from app.pages.memory_agent.graph import graph


class AgentWithMemory(BaseAIAgentChat):
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

        stream_response = self.graph.stream(
            input={"messages": input_messages},
            config=graph_config,
            stream_mode="messages",
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream_langgraph_messages(stream_response))

        st.session_state[f"{self.name}_messages"].append(
            {"role": "assistant", "content": response}
        )
        st.session_state[f"{self.name}_user_input_is_enabled"] = True


agent_with_memory = AgentWithMemory(
    title="AI Agent with Memory",
    name="ai_agent_with_memory",
    graph=graph,
    description="This agent can remember previous interactions and use them to provide better responses.",
    system_message=GENERAL_PURPOSE_AGENT_SYSTEM_PROMPT,
)

agent_with_memory.run()
