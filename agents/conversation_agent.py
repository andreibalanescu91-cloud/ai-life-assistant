from agents.emotion_agent import detect_emotion
from memory.memory_db import store_memory, retrieve_memory
from agents.reasoning_agent import analyze_problem
from memory.journal_db import save_entry


def process_message(message: str, user_id: str) -> str:
    """
    Full pipeline for a single user message, scoped to a specific user.
      1. Detect emotion
      2. Retrieve relevant memories for this user
      3. Generate advice + plan in ONE Claude API call
      4. Persist message to this user's memory and journal
      5. Return formatted response
    """
    emotion = detect_emotion(message)
    memories = retrieve_memory(message, user_id=user_id)
    analysis, plan = analyze_problem(message, emotion, memories)

    store_memory(message, user_id=user_id)
    save_entry(message, user_id=user_id)

    if plan:
        return f"{analysis}\n\n**Improvement Plan:**\n{plan}"
    return analysis
