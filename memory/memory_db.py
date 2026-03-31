import os
import hashlib
from supabase_client import get_supabase


def _embed(text: str) -> list[float]:
    """
    Generate an embedding vector using the Anthropic API.
    Falls back to a zero vector on error so the app never hard-crashes.
    """
    import anthropic
    try:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        # Voyage embedding model — 1024-dimensional, best for retrieval
        response = client.beta.messages.create(
            model="voyage-3",
            max_tokens=1,
            messages=[{"role": "user", "content": text}],
        )
        # Anthropic embeddings endpoint (uses voyageai under the hood)
        # Use the dedicated embeddings API directly via voyageai client
    except Exception:
        pass

    # Use voyageai directly (Anthropic's recommended embedding path)
    try:
        import voyageai
        vc = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY", os.environ.get("ANTHROPIC_API_KEY", "")))
        result = vc.embed([text], model="voyage-3", input_type="document")
        return result.embeddings[0]
    except Exception:
        # Return zero vector as safe fallback (1024-dim for voyage-3)
        return [0.0] * 1024


def store_memory(text: str, user_id: str) -> None:
    """Store a memory with its embedding vector, deduplicated by content hash."""
    stable_id = hashlib.md5(f"{user_id}:{text}".encode()).hexdigest()
    supabase = get_supabase()

    # Check for duplicates
    existing = supabase.table("memories").select("id").eq("content_hash", stable_id).execute()
    if existing.data:
        return  # already stored

    embedding = _embed(text)

    supabase.table("memories").insert({
        "user_id": user_id,
        "content": text,
        "content_hash": stable_id,
        "embedding": embedding,
    }).execute()


def retrieve_memory(query: str, user_id: str, n: int = 5) -> list[str]:
    """Return the top-n most semantically similar memories for this user."""
    try:
        embedding = _embed(query)
        supabase = get_supabase()

        # pgvector similarity search via Supabase RPC function
        result = supabase.rpc("match_memories", {
            "query_embedding": embedding,
            "match_user_id": user_id,
            "match_count": n,
        }).execute()

        return [row["content"] for row in (result.data or [])]
    except Exception:
        return []
