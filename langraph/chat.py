from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chat_bot(state: State):
    print("\n\n\nIn chat_bot:", id(state))
    print("\n\n\nChat_bot Node Added", state)
    response = llm.invoke(state.get("messages"))
    return {"messages": response}

def sample_node(state: State):
    print("\n\n\nIn sample_node", id(state))
    print("\n\n\nsample_node Called", state)
    return {"messages": ["Comming From Sample Node"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hey myself Muhammad Khusham Ali"]}))

print(f"\n\n\nUpdate State: {id(updated_state)}")
print(f"\n\n\nUpdate State: {updated_state}")