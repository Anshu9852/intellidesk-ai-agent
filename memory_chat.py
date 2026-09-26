"""
memory_chat.py
----------------
Yeh 'chat.py' ka upgraded version hai — ab agent ko purani
conversation yaad rehti hai, isliye follow-up sawaal bhi samajh
paayega.

Try karke dekhein:
  Aap: Notice period kitna hai?
  IntelliDesk: (batayega 60 din / 15 din)
  Aap: aur probation walon ke liye?
  IntelliDesk: (samajh jaayega ki "probation" ka reference
                pichle sawal se hai)
"""

from rag_pipeline import load_and_split_pdf, build_vector_store, answer_with_memory, PDF_PATH
from memory import ConversationMemory


def start_memory_chat():
    print("=" * 50)
    print("IntelliDesk — HR Document Assistant (with Memory)")
    print("=" * 50)
    print("\nPDF load ho rahi hai, thoda wait karein...\n")

    chunks = load_and_split_pdf(PDF_PATH)
    vector_store = build_vector_store(chunks)
    memory = ConversationMemory(max_turns=5)

    print("\nTaiyar hain! Ab yeh agent purani baatein yaad rakhega.")
    print("Chat khatam karne ke liye 'exit' ya 'quit' type karein.\n")

    while True:
        user_question = input("Aap: ")

        if user_question.lower() in ["exit", "quit", "bye"]:
            print("\nDhanyavaad! Chat khatam.")
            break

        if not user_question.strip():
            continue

        print("\nSoch rahe hain (purani baatein yaad karke)...")

        memory_context = memory.get_context_string()
        answer = answer_with_memory(user_question, vector_store, memory_context)
        memory.add_turn(user_question, answer)

        print(f"\nIntelliDesk: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    start_memory_chat()