"""
llm_client.py
--------------
Yeh file "LLM API" concept use karti hai (Course Section 111-114).

Yahan hum Google Gemini se connect karte hain. Yeh humare agent ka
"dimaag" hai - yahi actual mein sochkar jawab deta hai.

ZAROORI: Isko chalane ke liye ek GEMINI_API_KEY chahiye hogi .env
file mein. Bina key ke yeh error dega (yeh normal hai, jab tak
key nahi hai).
"""

import os
from dotenv import load_dotenv
from google import genai

# .env file se API key load karta hai
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def get_llm_response(prompt: str) -> str:
    """
    Yeh function ek prompt (text) leta hai, Gemini ko bhejta hai,
    aur uska jawab wapas deta hai.

    Abhi ke liye simple hai - baad mein isme document context
    bhi add karenge (RAG wale step mein).
    """
    if not API_KEY or API_KEY == "yahan_apni_key_paste_karo":
        return (
            "ERROR: API key set nahi hai. Pehle .env file mein "
            "apni GEMINI_API_KEY daalo, tabhi yeh function kaam karega."
        )

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # free tier ke liye fast model
        contents=prompt,
    )
    return response.text


# ---- Test karke dekhne ke liye ----
if __name__ == "__main__":
    test_prompt = "Hindi mein ek line mein batao: Python kya hai?"
    print("Prompt bhej rahe hain Gemini ko...")
    print("Response:", get_llm_response(test_prompt))
