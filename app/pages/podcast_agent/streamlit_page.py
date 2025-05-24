from typing import Any

import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.agents.AIModelSingleton import AIModelSingleton
from app.pages.podcast_agent.constants import NewsTopics
from app.pages.podcast_agent.graph import build_graph


class PodcastAgentStreamlitPage:
    def __init__(self):
        self.graph_model = st.session_state.ai_model_id
        self.graph = self.get_graph()
        self.name = "podcast_agent"

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

        news_topic_key = st.selectbox(
            label="Select a topic",
            options=[topic for topic in NewsTopics.__members__.keys()],
        )

        generate_podcast_button_is_enabled = self.get_session_state_value(
            "generate_podcast_button_is_enabled", True
        )

        generate_podcast_button = st.button(
            "Generate podcast script",
            disabled=not generate_podcast_button_is_enabled,
        )

        if generate_podcast_button:
            with st.status("Generating podcast script...", expanded=True):
                self.set_session_state_value(
                    "generate_podcast_button_is_enabled", False
                )

                self.generate_podcast(news_topic_key)

    def generate_podcast(self, news_topic_key: str):
        stream_response = self.graph.astream(
            input={"topic": NewsTopics[news_topic_key], "limit": 2},
            stream_mode="messages",
        )

        with st.chat_message("assistant"):
            response = st.write_stream(self.stream_langgraph_messages(stream_response))

        self.get_session_state_value("messages").append(
            {
                "content": response,
                "role": "assistant",
            }
        )

        self.set_session_state_value("generate_podcast_button_is_enabled", True)

        st.rerun()

    async def stream_langgraph_messages(self, stream_response):
        async for chunk, metadata in stream_response:
            if metadata["langgraph_node"] == "generate_podcast_script":
                yield chunk

    def run(self):
        if self.graph_model != st.session_state.ai_model_id:
            self.graph_model = st.session_state.ai_model_id
            self.graph = self.get_graph()

        self.display_page_content()


if "podcast_agent_instance" not in st.session_state:
    st.session_state.podcast_agent_instance = PodcastAgentStreamlitPage()

st.session_state.podcast_agent_instance.run()
