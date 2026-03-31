import re

# Expanded keyword lists — more real-world coverage per emotion
EMOTION_KEYWORDS: dict[str, list[str]] = {
    "stress": [
        "stress", "stressed", "overwhelmed", "pressure", "anxious", "anxiety",
        "burnout", "burnt out", "exhausted", "tense", "worried", "worrying",
        "panic", "panicking", "nervous", "dread", "dreading",
    ],
    "sadness": [
        "sad", "depressed", "depression", "unhappy", "lonely", "hopeless",
        "miserable", "heartbroken", "disappointed", "grief", "grieving",
        "lost", "empty", "numb", "crying", "cried", "worthless",
    ],
    "anger": [
        "angry", "anger", "frustrated", "frustrating", "furious", "annoyed",
        "rage", "irritated", "livid", "mad", "resentful", "bitter",
        "hate", "unfair", "outraged",
    ],
    "happiness": [
        "happy", "happiness", "excited", "grateful", "joyful", "great",
        "fantastic", "wonderful", "amazing", "thrilled", "proud", "content",
        "calm", "peaceful", "blessed", "love", "loved", "hopeful",
    ],
}


def detect_emotion(text: str) -> str:
    """
    Return the dominant emotion in text, or 'neutral' if none detected.
    Uses whole-word matching so 'mad' won't match inside 'made'.
    """
    lower = text.lower()
    scores: dict[str, int] = {emotion: 0 for emotion in EMOTION_KEYWORDS}

    for emotion, words in EMOTION_KEYWORDS.items():
        for word in words:
            # \b ensures whole-word match — avoids false positives
            if re.search(rf"\b{re.escape(word)}\b", lower):
                scores[emotion] += 1

    best = max(scores, key=lambda e: scores[e])
    return best if scores[best] > 0 else "neutral"