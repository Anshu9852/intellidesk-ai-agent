import os
from typing import TypedDict
from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, START, END

from rag_pipeline import load_and_split_pdf, build_vector_store, answer_question, PDF_PATH

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


class AgentState(TypedDict):
    question: str
    route: str
    answer: str


print("PDF load ho rahi hai, graph taiyar ho raha hai...")
chunks = load_and_split_pdf(PDF_PATH)
vector_store = build_vector_store(chunks)
print("Graph taiyar hai.\n")


def decide_node(state: AgentState) -> AgentState:
    print(f"[Node: decide] Sawal check ho raha hai -> '{state['question']}'")

    prompt = f"""Neeche diya gaya sawal padho aur bas ek word mein jawab do:
- Agar sawal HR policy, leave, reimbursement, notice period, company rules
  jaise document-related topics ke baare mein hai, toh likho: DOCUMENT
- Agar sawal general knowledge ke baare mein hai, toh likho: GENERAL

Sawal: {state['question']}

Sirf ek word likho: DOCUMENT ya GENERAL"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    decision = response.text.strip().upper()
    route = "document" if "DOCUMENT" in decision else "general"

    print(f"[Node: decide] Decision aaya -> {route}")
    return {"route": route}


def document_answer_node(state: AgentState) -> AgentState:
    print("[Node: document_answer] PDF se answer dhoonda ja raha hai...")
    answer = answer_question(state["question"], vector_store)
    return {"answer": answer}


def general_answer_node(state: AgentState) -> AgentState:
    print("[Node: general_answer] General knowledge se jawab diya ja raha hai...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=state["question"],
    )
    return {"answer": response.text.strip()}


def route_decision(state: AgentState) -> str:
    return state["route"]


builder = StateGraph(AgentState)
builder.add_node("decide", decide_node)
builder.add_node("document_answer", document_answer_node)
builder.add_node("general_answer", general_answer_node)

builder.add_edge(START, "decide")
builder.add_conditional_edges(
    "decide",
    route_decision,
    {"document": "document_answer", "general": "general_answer"},
)
builder.add_edge("document_answer", END)
builder.add_edge("general_answer", END)

graph = builder.compile()


if __name__ == "__main__":
    test_questions = [
        "reimbursement kaise milta hai",
        "France ki capital kya hai",
    ]

    for q in test_questions:
        print("=" * 50)
        result = graph.invoke({"question": q, "route": "", "answer": ""})
        print(f"\nQ: {q}")
        print(f"A: {result['answer']}")
        print("=" * 50)
        print()