from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from typing import Optional, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()

class State(TypedDict):
    input_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chat_bot(state: State):
    print("\nCalling chat_bot", state)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": state.get("input_query")}
        ]
    )
    return {"llm_output": response.choices[0].message.content}

def evaluation(state: State) -> Literal["exit", "reconstruction_bot"]:
    print("Calling Evaluation:", state)
    class Output_formate(BaseModel):
        is_good: bool = Field(..., description="Is the LLM output is good")
    
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format=Output_formate,
        messages=[
            {"role":"user", "content":f"Is it good {state.get("llm_output")}?"}
        ]
    )
    is_good = response.choices[0].message.parsed.is_good
    print(f"evaluation res: {response.choices[0].message.parsed}")

    if is_good:
        return "exit"
    return "reconstruction_bot"

def reconstruction_bot(state: State):
    print("Reconstruction Called: ", state)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": f"Re evaluate it {state.get("llm_output")} according to {state.get("input_query")}"}
        ]
    )
    return {"llm_output": response.choices[0].message.content}

def exit(state: State):
    print("Exit Called", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("evaluation", evaluation)
graph_builder.add_node("reconstruction_bot", reconstruction_bot)
graph_builder.add_node("exit", exit)


graph_builder.add_edge(START, "chat_bot")
graph_builder.add_conditional_edges("chat_bot", evaluation)
graph_builder.add_edge("reconstruction_bot", "exit")
graph_builder.add_edge("exit", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"input_query": "What is 1 - 2"}))
print(f"Updated State: {updated_state}")