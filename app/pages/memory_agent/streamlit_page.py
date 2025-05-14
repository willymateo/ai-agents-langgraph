import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

from app.pages.memory_agent.graph import graph
from app.utils.streaming import stream_langgraph_messages

st.title("AI Agent with memory")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("What do you want to ask the AI?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    stream_response = graph.stream(
        input={
            "messages": [
                SystemMessage("You are a helpful assistant"),
                HumanMessage(user_input),
            ]
        },
        config={"configurable": {"thread_id": "1234"}},
        stream_mode="messages",
    )

    response = ""

    with st.chat_message("assistant"):
        response = st.write_stream(stream_langgraph_messages(stream_response))

    st.session_state.messages.append({"role": "assistant", "content": response})
