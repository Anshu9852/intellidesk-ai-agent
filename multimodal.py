"""
multimodal.py
---------------
Yeh file "Multimodal Agent" concept use karti hai
(Course Section 163-164: Sending Multimedia to LLM - Images).

Ab tak humara agent sirf TEXT samajhta tha (PDF ka text). Ab hum
usse IMAGE bhi "dikha" rahe hain — jaise ek org chart — aur usse
poochh rahe hain uske baare mein sawaal.

Yeh kaam karta hai kyunki Gemini ek "multimodal" model hai — matlab
yeh text aur images, dono samajh sakta hai ek saath.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

IMAGE_PATH = "data/image_org_chart.png"


def ask_about_image(image_path: str, question: str) -> str:
    """
    Yeh function ek image aur ek sawaal leta hai, Gemini ko bhejta
    hai, aur jawab wapas deta hai.
    """
    client = genai.Client(api_key=API_KEY)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            question,
        ],
    )
    return response.text


# ---- Test karke dekhne ke liye ----
if __name__ == "__main__":
    print("Image ke baare mein Gemini se sawaal poochh rahe hain...\n")

    test_questions = [
        "Is image mein CEO ka naam kya hai?",
        "VP Engineering kaun hai aur unke neeche kaun kaam karta hai?",
        "Company mein total kitne employees hain?",
        "Is image ko ek line mein describe karo.",
    ]

    for q in test_questions:
        print(f"Q: {q}")
        answer = ask_about_image(IMAGE_PATH, q)
        print(f"A: {answer}\n")
        print("-" * 50)