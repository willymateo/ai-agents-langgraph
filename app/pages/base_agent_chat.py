from abc import ABC, abstractmethod
from typing import Any

import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.graph import CompiledGraph

from app.agents.utils.streaming import astream_langgraph_messages


class AgentChatPage(ABC):
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
        self.graph_model = st.session_state.ai_model_id
        self.graph = graph
        self.title = title
        self.name = name

        self.initialize_session_state()

    @abstractmethod
    def get_graph(self) -> CompiledGraph:
        pass

    def get_session_state_value(self, parameter_name: str, default_value: Any = None):
        return st.session_state.get(f"{self.name}_{parameter_name}", default_value)

    def set_session_state_value(self, parameter_name: str, value: Any):
        st.session_state[f"{self.name}_{parameter_name}"] = value

    def initialize_session_state(self):
        messages = self.get_session_state_value("messages")
        user_input_is_enabled = self.get_session_state_value("user_input_is_enabled")

        if messages is None:
            self.set_session_state_value("messages", [])

        if user_input_is_enabled is None:
            self.set_session_state_value("user_input_is_enabled", True)

    def display_page_content(self):
        st.title(self.title)

        if self.description:
            st.info(self.description, icon="ℹ️")

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

    def on_user_input(self, user_input):
        self.set_session_state_value("user_input_is_enabled", False)
        self.get_session_state_value("messages", []).append(
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

        stream_response = self.graph.astream(
            input={"messages": input_messages},
            stream_mode="messages",
        )

        with st.chat_message("assistant"):
            response = st.write_stream(astream_langgraph_messages(stream_response))
            self.set_session_state_value("user_input_is_enabled", True)

        self.get_session_state_value("messages", []).append(
            {
                "role": "assistant",
                "content": response,
            }
        )

    def run(self):
        if self.graph_model != st.session_state.ai_model_id:
            self.graph_model = st.session_state.ai_model_id
            self.graph = self.get_graph()

        self.display_page_content()


class AgentChatWithMemoryPage(AgentChatPage):
    def on_user_input(self, user_input):
        self.set_session_state_value("user_input_is_enabled", False)
        self.get_session_state_value("messages", []).append(
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
            stream_mode="messages",
            config=graph_config,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(astream_langgraph_messages(stream_response))
            self.set_session_state_value("user_input_is_enabled", True)

        self.get_session_state_value("messages", []).append(
            {
                "role": "assistant",
                "content": response,
            }
        )
