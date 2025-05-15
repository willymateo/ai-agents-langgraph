import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.graph import CompiledGraph

from app.agents.utils.streaming import stream_langgraph_messages


class BaseAIAgentChat:
    def __init__(
        self,
        title: str,
        name: str,
        graph: CompiledGraph,
        description: str = "",
        system_message: str = "",
    ):
        self.system_message = system_message
        self.description = description
        self.graph = graph
        self.title = title
        self.name = name

        self.initialize_session_state()

    def initialize_session_state(self):
        messages_key = f"{self.name}_messages"
        user_input_is_disabled_key = f"{self.name}_user_input_is_enabled"

        if messages_key not in st.session_state:
            st.session_state[messages_key] = []

        if user_input_is_disabled_key not in st.session_state:
            st.session_state[user_input_is_disabled_key] = True

    def display_page_content(self):
        st.title(self.title)

        if self.description:
            st.info(self.description, icon="ℹ️")

        for message in st.session_state[f"{self.name}_messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input(
            "What do you want to ask the AI?",
            disabled=not st.session_state[f"{self.name}_user_input_is_enabled"],
        )

        if user_input:
            self.on_user_input(user_input)

    def on_user_input(self, user_input):
        st.session_state[f"{self.name}_user_input_is_enabled"] = False
        st.session_state[f"{self.name}_messages"].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        input_messages = [HumanMessage(user_input)]

        if self.system_message:
            input_messages = [
                SystemMessage(self.system_message),
                HumanMessage(user_input),
            ]

        stream_response = self.graph.stream(
            input={"messages": input_messages},
            stream_mode="messages",
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream_langgraph_messages(stream_response))

        st.session_state[f"{self.name}_messages"].append(
            {"role": "assistant", "content": response}
        )
        st.session_state[f"{self.name}_user_input_is_enabled"] = True

    def run(self):
        self.display_page_content()
