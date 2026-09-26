"""
models.py
----------
Yeh file "Pydantic" concept use karti hai (Course Section 89-101).

Pydantic kya karta hai: yeh ensure karta hai ki data hamesha sahi
"shape" (format) mein rahe. Jaise agar hum keh dein ki "question"
hamesha ek string honi chahiye, toh Pydantic khud check kar lega —
agar koi galat type ka data aayega, error de dega.

Isse hamara AI agent "garbage in, garbage out" wali problem se bacha
rahega.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Question(BaseModel):
    """
    User jab bhi document ke baare mein kuch poochega,
    uska data isी shape mein aayega.
    """
    text: str = Field(..., description="User ka actual sawal")
    session_id: str = Field(..., description="Kis conversation ka hissa hai yeh sawal")
    timestamp: datetime = Field(default_factory=datetime.now)


class SourceChunk(BaseModel):
    """
    Jab document se koi paragraph/chunk answer ke liye use hota hai,
    uski detail yeh model store karega — taaki hum bata sakein
    "yeh answer document ke kis page/part se aaya hai".
    """
    content: str
    page_number: Optional[int] = None
    source_file: str


class Answer(BaseModel):
    """
    Agent ka final response is shape mein hoga.
    """
    text: str = Field(..., description="Agent ka jawab")
    sources: list[SourceChunk] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    session_id: str


# ---- Yeh code khud test karke dekhne ke liye ----
if __name__ == "__main__":
    # Ek sample question banate hain
    q = Question(text="HR leave policy kya hai?", session_id="abc123")
    print("Question object bana:", q)

    # Agar galat data denge, Pydantic error dega (isse try karke dekho)
    try:
        bad_question = Question(text=123, session_id="abc123")  # text string honi chahiye thi
    except Exception as e:
        print("\nPydantic ne error pakda (yeh sahi hai):")
        print(e)
