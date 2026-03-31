from memory.journal_db import get_entries

KEYWORDS: dict[str, list[str]] = {
    "stress":    ["stress", "overwhelmed", "pressure", "anxious", "burnout",
                  "exhausted", "nervous", "worried", "panic", "tense"],
    "sadness":   ["sad", "depressed", "unhappy", "lonely", "hopeless",
                  "miserable", "heartbroken", "empty", "numb", "grief"],
    "anger":     ["angry", "frustrated", "furious", "annoyed", "rage",
                  "irritated", "resentful", "bitter", "hate", "outraged"],
    "happiness": ["happy", "excited", "grateful", "joyful", "great",
                  "fantastic", "wonderful", "thrilled", "proud", "content"],
}


def detect_patterns() -> dict:
    """
    Return emotion counts across all journal entries.

    Each entry contributes at most 1 to each emotion bucket (avoids one
    very long entry dominating the chart).  Entries are returned newest-first
    from ChromaDB, so no extra sorting is needed for display.
    """
    docs, metadatas = get_entries()

    if not docs:
        return {
            "stress": 0,
            "sadness": 0,
            "anger": 0,
            "happiness": 0,
            "total_entries": 0,
        }

    counts: dict[str, int] = {emotion: 0 for emotion in KEYWORDS}

    for doc in docs:
        lower = doc.lower()
        for emotion, words in KEYWORDS.items():
            # One hit per entry per emotion — avoids length bias
            if any(word in lower for word in words):
                counts[emotion] += 1

    counts["total_entries"] = len(docs)
    return counts