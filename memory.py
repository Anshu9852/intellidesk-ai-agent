"""
memory.py
----------
Yeh file "Memory in AI Agents" concept use karti hai
(Course Section 177-188).

Types of memory jo course mein sikhaye gaye:
- Short-Term Memory (Section 180): Abhi ki conversation ka context
  (jaise pichle 5 messages)
- Long-Term Memory (Section 181): Persistent knowledge jo session
  khatam hone ke baad bhi rehti hai

Yahan hum SHORT-TERM memory implement kar rahe hain — conversation
ke dauraan pichle sawal-jawab yaad rakhna, taaki follow-up sawaal
samajh mein aayein.
"""


class ConversationMemory:
    """
    Yeh class conversation ka history store karti hai — jaise ek
    notebook jisme har sawal-jawab likha jaata hai.
    """

    def __init__(self, max_turns: int = 5):
        """
        'max_turns=5' matlab sirf pichle 5 sawal-jawab yaad rakhenge.
        """
        self.history = []
        self.max_turns = max_turns

    def add_turn(self, question: str, answer: str):
        """Ek naya sawal-jawab memory mein add karta hai."""
        self.history.append({"question": question, "answer": answer})

        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context_string(self) -> str:
        """
        Poori memory ko ek text ke roop mein deta hai, jise hum
        prompt mein daal sakein taaki LLM ko purani baatein pata ho.
        """
        if not self.history:
            return "(Koi purani conversation nahi hai)"

        context_lines = []
        for turn in self.history:
            context_lines.append(f"User: {turn['question']}")
            context_lines.append(f"Assistant: {turn['answer']}")

        return "\n".join(context_lines)

    def clear(self):
        """Memory ko poora khali kar deta hai."""
        self.history = []