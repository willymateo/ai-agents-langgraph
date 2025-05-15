from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

llm_model = ChatOllama(model="deepseek-r1:8b", temperature=0.1)


@tool
def call_api():
    """
    Call an API and return the result.
    """
    return "API response"


tools = [call_api]

llm_with_tools = llm_model.bind_tools(tools)


def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": response}


workflow = StateGraph(state_schema=MessagesState)

# Add nodes
workflow.add_node("assistant", call_model)
workflow.add_node("tools", ToolNode(tools))

# Add edges
workflow.set_entry_point("assistant")
workflow.add_conditional_edges("assistant", tools_condition)
workflow.add_edge("tools", "assistant")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
