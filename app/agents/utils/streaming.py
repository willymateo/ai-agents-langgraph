from langchain_core.messages import AIMessage


async def astream_langgraph_messages(stream):
    async for chunk, _ in stream:
        if isinstance(chunk, AIMessage):
            yield chunk.content
