import chromadb
import hashlib
from datetime import datetime

# PersistentClient keeps data on disk across restarts
client = chromadb.PersistentClient(path="./chroma_data")

try:
    journal_collection = client.get_collection("journal")
except Exception:
    journal_collection = client.create_collection("journal")


def save_entry(text: str) -> None:
    """Save a journal entry with a stable, unique ID."""
    # Combine text + timestamp so identical messages on different days are distinct
    raw = f"{text}_{datetime.now().isoformat()}"
    entry_id = hashlib.md5(raw.encode()).hexdigest()

    journal_collection.add(
        documents=[text],
        metadatas=[{"date": str(datetime.now())}],
        ids=[entry_id],
    )


def get_entries(query: str | None = None, n: int = 10):
    """Return (documents, metadatas). Optionally filter by semantic query."""
    if query:
        results = journal_collection.query(
            query_texts=[query],
            n_results=n,
        )
        return results["documents"][0], results["metadatas"][0]

    results = journal_collection.get()
    return results["documents"], results["metadatas"]