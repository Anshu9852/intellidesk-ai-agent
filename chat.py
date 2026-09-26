"""
chat.py
--------
Yeh file interactive chat banati hai — ab fixed sawaal nahi,
aap khud jo bhi poochhna chahein, type kar sakti hain.

Yeh 'rag_pipeline.py' mein jo functions banaye the (load_and_split_pdf,
build_vector_store, answer_question), unhi ko yahan reuse kar rahe hain
— naya code dobara nahi likha, sirf import kiya (Section 47: Python
Imports/Modules ka concept).
"""

from rag_pipeline import load_and_split_pdf, build_vector_store, answer_question, PDF_PATH


def start_chat():
    print("=" * 50)
    print("IntelliDesk — HR Document Assistant")
    print("=" * 50)
    print("\nPDF load ho rahi hai, thoda wait karein...\n")

    chunks = load_and_split_pdf(PDF_PATH)
    vector_store = build_vector_store(chunks)

    print("\nTaiyar hain! Ab aap apna sawal poochh sakti hain.")
    print("Chat khatam karne ke liye 'exit' ya 'quit' type karein.\n")

    while True:
        user_question = input("Aap: ")

        if user_question.lower() in ["exit", "quit", "bye"]:
            print("\nDhanyavaad! Chat khatam.")
            break

        if not user_question.strip():
            continue

        print("\nSoch rahe hain...")
        answer = answer_question(user_question, vector_store)
        print(f"\nIntelliDesk: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    start_chat()