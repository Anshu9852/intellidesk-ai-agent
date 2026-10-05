import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel

from rag_pipeline import load_and_split_pdf, build_vector_store, answer_question, PDF_PATH

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini ko OpenAI-compatible endpoint se access karna
gemini_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-3.6-flash",
    openai_client=gemini_client,
)

# PDF ek hi baar load karna
print("PDF load ho rahi hai...")
chunks = load_and_split_pdf(PDF_PATH)
vector_store = build_vector_store(chunks)
print("Taiyar hai.\n")


# ---- TOOL define karna ----
# @function_tool decorator se yeh function agent ko "tool" ke roop mein
# available ho jata hai. Docstring padh kar agent khud samajhta hai
# yeh tool kab use karna hai.

@function_tool
def search_company_policy(question: str) -> str:
    """Company ki HR policy document (leave, reimbursement, notice period,
    jaise topics) se related sawaalon ka jawab dhoondhta hai. Jab bhi
    sawal company rules ke baare mein ho, yeh tool use karo."""
    return answer_question(question, vector_store)


# ---- AGENT banana ----

agent = Agent(
    name="IntelliDesk Assistant",
    instructions=(
        "Tum ek helpful HR assistant ho. Agar sawal company policy "
        "(leave, reimbursement, notice period, etc.) se related hai, "
        "toh 'search_company_policy' tool use karo. Agar general "
        "knowledge ka sawal hai, toh seedha apne knowledge se jawab do."
    ),
    model=model,
    tools=[search_company_policy],
)


async def ask(question: str) -> str:
    result = await Runner.run(agent, question)
    return result.final_output


async def main():
    test_questions = [
        "reimbursement kaise milta hai",
        "France ki capital kya hai",
    ]

    for q in test_questions:
        print("=" * 50)
        answer = await ask(q)
        print(f"\nQ: {q}")
        print(f"A: {answer}")
        print("=" * 50)
        print()


if __name__ == "__main__":
    asyncio.run(main())