import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="IntelliDesk API")

CONTEXT = "Notice period: confirmed employees ke liye 60 din, probation walon ke liye 15 din."


class Question(BaseModel):
    question: str


def ask_gemini(prompt):
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash", contents=prompt
            )
            return response.text
        except Exception:
            time.sleep(10)
    return "Server abhi busy hai, thodi der baad try kariye."


@app.get("/")
def home():
    return {"status": "IntelliDesk API chal rahi hai"}


@app.post("/ask")
def ask(body: Question):
    prompt = f"""Tum ek friendly HR assistant ho jo naye employees se aaram se baat karta hai.
Neeche example dekho, phir usi chhote style mein jawab do.

Sawal: Confirmed employee ka notice period?
Jawab: 60 din.

Document: {CONTEXT}
Sawal: {body.question}
Jawab:"""
    answer = ask_gemini(prompt).replace("Jawab:", "").strip()
    return {"question": body.question, "answer": answer}