from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph


def build_graph(model: BaseChatModel):
    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])

        return {"messages": response}

    # Graph
    workflow = StateGraph(state_schema=MessagesState)

    # Add nodes
    workflow.add_node("assistant", call_model)

    # Add edges
    workflow.set_entry_point("assistant")

    checkpointer = MemorySaver()
    return workflow.compile(name="memory_agent", checkpointer=checkpointer)
