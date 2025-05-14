from langchain_core.messages import AIMessage


def stream_langgraph_messages(stream):
    for chunk, _ in stream:
        if isinstance(chunk, AIMessage):
            yield chunk.content
