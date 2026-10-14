import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)

for model in ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.1-flash-lite"]:
    print("Try kar rahe hain:", model)
    try:
        r = client.models.generate_content(model=model, contents="Hindi mein ek line: Python kya hai?")
        print("CHAL RAHA HAI ->", r.text, "\n")
    except Exception as e:
        print("FAIL ->", str(e)[:150], "\n")