# IntelliDesk — AI Document Assistant (Starter Project)

Yeh ek AI agent project hai jo document upload karke uspar sawal-jawab
karne deta hai. Yeh MCA/BCA resume ke liye "Agentic AI + GenAI" project
ke roop mein banaya ja raha hai.

## Abhi tak kya bana hai (Phase 1)

| File | Kaam | Course Concept |
|---|---|---|
| `models.py` | Data ka structure define karta hai (Question, Answer, SourceChunk) | Pydantic (Section 89-101) |
| `llm_client.py` | Google Gemini se connect karke jawab leta hai | LLM API (Section 111-114) |

## Setup kaise karein (VS Code mein)

### Step 1: Python install check karo
Terminal mein: `python3 --version` (3.10+ hona chahiye)

### Step 2: Virtual environment banao (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### Step 3: Libraries install karo
```bash
pip install -r requirements.txt
```

### Step 4: API key set karo
1. `.env.example` file ko copy karke naam do `.env`
2. Us `.env` file ke andar apni Gemini API key paste karo:
   ```
   GEMINI_API_KEY=AIzaSy........
   ```
3. Key kaise banayein: https://aistudio.google.com → "Get API Key"

### Step 5: Test karo
```bash
python3 models.py       # Pydantic models test karega
python3 llm_client.py   # Gemini se connect karke ek jawab layega
```

Agar `llm_client.py` chalane par ek Hindi sentence mil jaye ("Python ek
programming language hai" jaisa kuch) — matlab sab sahi set ho gaya hai!

## Aage kya banega (roadmap)

- [ ] Phase 2: PDF upload aur document padhna (RAG — Section 143-153)
- [ ] Phase 3: Document ko chunks mein todkar vector database mein store karna
- [ ] Phase 4: Actual RAG pipeline — sawal ka jawab document se nikalna
- [ ] Phase 5: LangGraph se agent ka flow design (Section 165-176)
- [ ] Phase 6: Memory add karna — purani baatein yaad rakhna (Section 177-188)
- [ ] Phase 7: Streamlit se simple website/UI banana
- [ ] Phase 8: Docker + deployment (Section 218-250)

## Note

Yeh project course ka copy nahi hai — course ke concepts (Pydantic,
LLM APIs, RAG, LangGraph, Memory) seekhkar apna alag use-case
(document Q&A assistant) banaya ja raha hai.
