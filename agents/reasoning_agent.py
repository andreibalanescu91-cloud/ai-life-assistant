import os
import anthropic

# Client is initialised lazily so missing keys surface as a clean error message
_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Add it to your Streamlit Cloud secrets (Settings → Secrets)."
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def analyze_problem(message: str, emotion: str, memories: list[str]) -> tuple[str, str]:
    """
    Ask Claude for supportive advice AND an improvement plan in one API call.
    Returns (analysis, plan) as a tuple.
    """
    memory_text = "\n".join(f"- {m}" for m in memories) if memories else "None yet."

    prompt = f"""A user has shared something with you.

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
        client = _get_client()
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=(
                "You are a supportive AI life companion. "
                "You respond with empathy, warmth, and practical advice. "
                "Always follow the exact two-section format requested by the user."
            ),
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.content[0].text

        if "### Step-by-Step Improvement Plan" in raw:
            parts = raw.split("### Step-by-Step Improvement Plan", 1)
            analysis = parts[0].replace("### Supportive Advice", "").strip()
            plan = parts[1].strip()
        else:
            analysis = raw.strip()
            plan = ""

        return analysis, plan

    except RuntimeError as e:
        return str(e), ""
    except anthropic.AuthenticationError:
        return "Invalid API key. Check your Streamlit Cloud secrets.", ""
    except anthropic.RateLimitError:
        return "Rate limit reached. Please wait a moment and try again.", ""
    except Exception as e:
        return f"Unexpected error: {e}", ""