from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph

llm_model = ChatOllama(model="deepseek-r1:8b", temperature=0.1)


def call_model(state: MessagesState):
    response = llm_model.invoke(state["messages"])

    return {"messages": response}


workflow = StateGraph(state_schema=MessagesState)

# Add nodes
workflow.add_node("model", call_model)

# Add edges
workflow.set_entry_point("model")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
