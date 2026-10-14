import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask(prompt):
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash", contents=prompt
            )
            return response.text
        except Exception:
            time.sleep(10)
    return "Server abhi busy hai, thodi der baad try kariye."


context = "Notice period: confirmed employees ke liye 60 din, probation walon ke liye 15 din."
question = "Main probation mein hoon, mujhe kitne din ka notice dena hoga?"

# 1. Persona prompt
persona = f"""Tum ek friendly HR assistant ho jo naye employees se aaram se baat karta hai.
Document: {context}
Sawal: {question}
Chhota jawab do."""

# 2. Few-shot prompt (pehle example dikhate hain)
few_shot = f"""Neeche examples dekho, phir usi style mein jawab do.

Sawal: Confirmed employee ka notice period?
Jawab: 60 din.

Sawal: Probation mein notice period?
Jawab: 15 din.

Document: {context}
Sawal: {question}
Jawab:"""

# 3. Chain-of-Thought prompt (step-by-step sochna)
cot = f"""Document: {context}
Sawal: {question}
Pehle step-by-step sochkar batao (kaun si category hai, uska rule kya hai), phir aakhir mein final jawab likho."""

for name, prompt in [("PERSONA", persona), ("FEW-SHOT", few_shot), ("COT", cot)]:
    print("=" * 50)
    print(name)
    print("=" * 50)
    print(ask(prompt))
    print()