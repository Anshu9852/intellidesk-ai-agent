import os
import sys
import contextlib
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("IntelliDesk")


@mcp.tool()
def list_documents() -> list[str]:
    """data folder mein maujood saari files ki list deta hai."""
    return sorted(os.listdir("data"))


@mcp.tool()
def search_company_policy(question: str) -> str:
    """Company ki HR policy PDF se sawal ka jawab dhoondhta hai."""
    # rag_pipeline print karta hai; MCP mein print protocol bigadta hai, isliye stderr pe bhej rahe hain
    with contextlib.redirect_stdout(sys.stderr):
        from rag_pipeline import load_and_split_pdf, build_vector_store, answer_question, PDF_PATH
        chunks = load_and_split_pdf(PDF_PATH)
        store = build_vector_store(chunks)
        return answer_question(question, store)


if __name__ == "__main__":
    mcp.run()