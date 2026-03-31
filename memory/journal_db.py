from datetime import datetime
from supabase_client import get_supabase


def save_entry(text: str, user_id: str) -> None:
    """Save a journal entry for a specific user."""
    get_supabase().table("journal_entries").insert({
        "user_id": user_id,
        "content": text,
        "created_at": datetime.utcnow().isoformat(),
    }).execute()


def get_entries(user_id: str, query: str | None = None, n: int = 50):
    """
    Return (documents, metadatas) for a user.
    Basic keyword filter applied when query is provided (pgvector similarity
    search is handled in memory_db for the chat pipeline).
    """
    supabase = get_supabase()

    result = (
        supabase.table("journal_entries")
        .select("content, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(n)
        .execute()
    )

    rows = result.data or []
    docs = [r["content"] for r in rows]
    metas = [{"date": r["created_at"]} for r in rows]
    return docs, metas
