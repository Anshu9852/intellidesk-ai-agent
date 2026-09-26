"""
rag_pipeline.py
-----------------
Yeh file "RAG" (Retrieval-Augmented Generation) concept use karti hai
(Course Section 143-153).

RAG kya karta hai, simple bhasha mein:
1. PDF ko chhote-chhote tukdon (chunks) mein todte hain
2. Har chunk ko ek "embedding" (numbers ki list) mein convert karte hain
   jo uska matlab represent karti hai
3. In embeddings ko ek "vector database" mein store karte hain
4. Jab user sawal poochta hai, uske sawal ko bhi embedding mein badalte
   hain aur database mein sabse "milte-julte" (relevant) chunks dhoondhte
   hain
5. Wo relevant chunks + user ka sawal, dono LLM (Gemini) ko bhejte hain
   taaki wo accurate jawab de sake — sirf document ke content se

Isse LLM "hallucinate" nahi karta (galat/banayi hui baatein nahi
batata) - kyunki usse sirf document ka actual content diya ja raha hai.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

PDF_PATH = "data/company_policy.pdf"
VECTOR_STORE_PATH = "vector_store"


def load_and_split_pdf(pdf_path: str):
    """
    Step 1: PDF padhna aur chunks mein todna.

    'chunk_size=500' matlab har tukda lagbhag 500 characters ka hoga.
    'chunk_overlap=50' matlab consecutive chunks thoda overlap karenge,
    taaki koi important context beech mein na kat jaye.
    """
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(pages)

    print(f"PDF se total {len(chunks)} chunks bane.")
    return chunks


def build_vector_store(chunks):
    """
    Step 2 & 3: Chunks ko embeddings mein convert karke vector database
    (Chroma) mein store karna.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=API_KEY,
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH,
    )
    print("Vector store ban gaya aur save ho gaya.")
    return vector_store


def get_relevant_chunks(vector_store, query: str, k: int = 5):
    """
    Step 4: User ke sawal se sabse relevant chunks dhoondhna.
    'k=3' matlab top 3 sabse milte-julte chunks lenge.
    """
    results = vector_store.similarity_search(query, k=k)
    return results


def answer_question(query: str, vector_store) -> str:
    """
    Step 5: Relevant chunks + sawal, Gemini ko bhejkar final answer lena.
    """
    relevant_chunks = get_relevant_chunks(vector_store, query)

    # Saare relevant chunks ka text jodkar ek context bana rahe hain
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])

    prompt = f"""Tum ek helpful HR assistant ho. Neeche diye gaye document
ke content ke aadhar par hi user ke sawal ka jawab do. Agar document mein
answer nahi hai, toh saaf bol do "Yeh information document mein nahi hai."

Document Content:
{context}

User ka Sawal: {query}

Jawab (Hindi ya Hinglish mein, seedha aur clear):"""

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text


# ---- Test karke dekhne ke liye ----
if __name__ == "__main__":
    print("PDF load ho rahi hai aur process ho rahi hai...\n")
    chunks = load_and_split_pdf(PDF_PATH)
    vector_store = build_vector_store(chunks)

    print("\n--- Ab sawal poochte hain ---\n")

    test_questions = [
        "Annual leave kitne din milti hai?",
        "Notice period kitne din ka hai?",
        "Work from home ki policy kya hai?",
    ]

    for q in test_questions:
        print(f"Q: {q}")
        answer = answer_question(q, vector_store)
        print(f"A: {answer}\n")
        print("-" * 50)


def answer_with_memory(query: str, vector_store, memory_context: str = "") -> str:
    """
    Yeh 'answer_question' ka hi upgraded version hai — isme purani
    conversation ka context bhi add hota hai, taaki follow-up
    sawaalon ka matlab samajh aaye.

    (Course Section 180: Short-Term Memory — Context Windows)
    """
    relevant_chunks = get_relevant_chunks(vector_store, query)
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])

    prompt = f"""Tum ek helpful HR assistant ho. Neeche diye gaye document
ke content ke aadhar par hi user ke sawal ka jawab do. Agar document mein
answer nahi hai, toh saaf bol do "Yeh information document mein nahi hai."

Pichli Conversation (agar follow-up sawal hai toh yeh context use karo):
{memory_context}

Document Content:
{context}

User ka Naya Sawal: {query}

Jawab (Hindi ya Hinglish mein, seedha aur clear):"""

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text