from agents.emotion_agent import detect_emotion
from memory.memory_db import store_memory, retrieve_memory
from agents.reasoning_agent import analyze_problem
from memory.journal_db import save_entry


def process_message(message: str) -> str:
    """
    Full pipeline for a single user message:
      1. Detect emotion
      2. Retrieve relevant memories
      3. Generate advice + plan in ONE LLM call
      4. Persist the message to memory and journal
      5. Return the formatted response
    """
    emotion = detect_emotion(message)
    memories = retrieve_memory(message)

    # analyze_problem now returns (advice, plan) — one LLM call instead of two
    analysis, plan = analyze_problem(message, emotion, memories)

    store_memory(message)
    save_entry(message)

    if plan:
        return f"{analysis}\n\n**Improvement Plan:**\n{plan}"
    return analysis