from langgraph.graph import START,END, StateGraph


from app.models import State
from app.nodes import (
    classify_intent,
    retrieve_and_answer,
    direct_answer,
)

def route(state):
    
    print("\n========== ROUTER ==========")
    print("Intent received by router:", state["intent"])

    if state["intent"] == "policy_question":
        print("Routing to: retrieve_and_answer")
    else:
        print("Routing to: direct_answer")

    return state["intent"]

builder = StateGraph(State)

# nodes
builder.add_node("classify_intent",classify_intent)
builder.add_node("retrieve_and_answer",retrieve_and_answer)
builder.add_node("direct_answer",direct_answer)

# edges
builder.add_edge(START,"classify_intent")
builder.add_conditional_edges(
    "classify_intent",
    route,

    {
        "policy_question":"retrieve_and_answer",
        "general_question":"direct_answer"
    }
)
builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke(
        {
            "question": "Tell me a joke."
        }
    )
    print(result)