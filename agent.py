"""
agent.py
---------
Yeh file "Agentic AI" ka core concept use karti hai (Course Section
138-142: Agentic AI Fundamentals).

Ab tak humara code seedha document se answer nikal leta tha — koi
"decision" nahi leta tha. Yeh **asli agent nahi** hota.

Real Agent kya karta hai:
1. User ka sawal samajhta hai
2. KHUD DECIDE karta hai ki uska jawab dene ke liye kaunsa "tool"
   use karna sahi rahega
3. Wo tool chalata hai
4. Result ko final answer mein badalta hai

Humare agent ke paas 2 tools hain:
- "document_search": jab sawal company policy se related ho
- "general_knowledge": jab sawal document se related na ho

Decision khud LLM (Gemini) leta hai, structured output ke through
(Pydantic model use karke — Section 141: "Enforcing Structured
Outputs with Pydantic").
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal
from google import genai

from rag_pipeline import load_and_split_pdf, build_vector_store, answer_question, PDF_PATH

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


class ToolDecision(BaseModel):
    """
    Yeh structure define karta hai ki agent ka "decision" kaisa dikhega.
    Pydantic ensure karega ki LLM hamesha in do options mein se
    hi ek chune — kuch random/galat nahi.
    """
    tool_to_use: Literal["document_search", "general_knowledge"] = Field(
        ..., description="Kaunsa tool is sawal ke liye sahi hai"
    )
    reason: str = Field(..., description="Yeh tool kyun chuna, ek line mein")


def decide_tool(query: str) -> ToolDecision:
    """
    Yeh function agent ka "dimaag" hai — decide karta hai kaunsa
    tool chalana hai.
    """
    client = genai.Client(api_key=API_KEY)

    decision_prompt = f"""Tum ek AI agent ho jo decide karta hai ki
user ke sawal ka jawab kaise dena hai. Do options hain:

1. "document_search" — agar sawal company ki HR policy, leave,
   notice period, work from home, reimbursement, ya kisi bhi
   internal company rule se related ho
2. "general_knowledge" — agar sawal kisi general/duniya ke baare
   mein ho jiska company policy se koi lena dena na ho

User ka sawal: "{query}"

Sirf JSON format mein jawab do, is tarah:
{{"tool_to_use": "document_search" ya "general_knowledge", "reason": "chhota reason"}}"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=decision_prompt,
        config={"response_mime_type": "application/json"},
    )

    import json
    decision_data = json.loads(response.text)
    return ToolDecision(**decision_data)


def general_knowledge_answer(query: str) -> str:
    """
    Tool 2: Agar sawal document se related nahi hai, toh Gemini
    seedha apne general knowledge se jawab dega.
    """
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Is sawal ka seedha, chhota jawab do (Hindi/Hinglish mein): {query}",
    )
    return response.text


def run_agent(query: str, vector_store):
    """
    Yeh poore agent ka "brain" hai — decide karta hai aur phir
    sahi tool chalata hai.
    """
    print("Agent soch raha hai kaunsa tool use karna hai...")
    decision = decide_tool(query)
    print(f"Decision: '{decision.tool_to_use}' tool use karenge. Reason: {decision.reason}\n")

    if decision.tool_to_use == "document_search":
        answer = answer_question(query, vector_store)
    else:
        answer = general_knowledge_answer(query)

    return answer, decision.tool_to_use


# ---- Test karke dekhne ke liye ----
if __name__ == "__main__":
    print("PDF load ho rahi hai...\n")
    chunks = load_and_split_pdf(PDF_PATH)
    vector_store = build_vector_store(chunks)

    test_queries = [
        "Notice period kitne din ka hai?",          # document-related
        "Bharat ki capital kya hai?",                 # general knowledge
        "Reimbursement kaise claim karein?",          # document-related
    ]

    for q in test_queries:
        print(f"Q: {q}")
        answer, tool_used = run_agent(q, vector_store)
        print(f"A: {answer}")
        print(f"(Tool used: {tool_used})\n")
        print("-" * 50)