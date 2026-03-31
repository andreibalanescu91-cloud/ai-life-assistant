import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def analyze_problem(message: str, emotion: str, memories: list[str]) -> tuple[str, str]:
    """
    Ask the LLM for both supportive advice AND an improvement plan in one call.
    Returns (analysis, plan) as a tuple to avoid a second round-trip.
    """
    memory_text = "\n".join(f"- {m}" for m in memories) if memories else "None yet."

    prompt = f"""You are a supportive AI life companion. A user has shared something with you.

User message: {message}
Detected emotion: {emotion}
Relevant past memories:
{memory_text}

Please respond in two clearly labelled sections:

### Supportive Advice
Write 2-3 sentences of warm, empathetic support that acknowledges the emotion and context.

### Step-by-Step Improvement Plan
List 3-5 concrete, actionable steps the user can take to improve their situation.
"""

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()

        if "response" not in data:
            return f"Unexpected AI response: {data}", ""

        # Split on the plan header so we can return the two parts separately
        raw = data["response"]
        if "### Step-by-Step Improvement Plan" in raw:
            parts = raw.split("### Step-by-Step Improvement Plan", 1)
            analysis = parts[0].replace("### Supportive Advice", "").strip()
            plan = parts[1].strip()
        else:
            # Fallback: treat the whole response as advice
            analysis = raw.strip()
            plan = "No structured plan returned — try rephrasing your message."

        return analysis, plan

    except requests.exceptions.ConnectionError:
        return (
            "Could not reach Ollama. Make sure it is running on localhost:11434.",
            "",
        )
    except requests.exceptions.Timeout:
        return "Ollama timed out. The model may still be loading — please try again.", ""
    except Exception as e:
        return f"Unexpected error: {e}", ""