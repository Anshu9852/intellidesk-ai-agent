# tasks.py
# Yeh worker (chef) ki "recipe" file hai.

from rag_pipeline import load_and_split_pdf, build_vector_store


def process_pdf_task(pdf_path: str) -> dict:
    # 1. PDF load karke chunks banao
    chunks = load_and_split_pdf(pdf_path)

    # 2. Chunks ko embeddings banakar Chroma mein save karo
    build_vector_store(chunks)

    return {"status": "done", "file": pdf_path, "chunks": len(chunks)}