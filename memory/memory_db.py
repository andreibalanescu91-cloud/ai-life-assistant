import chromadb
import hashlib

# PersistentClient keeps data on disk across restarts
client = chromadb.PersistentClient(path="./chroma_data")

try:
    collection = client.get_collection("life_memory")
except Exception:
    collection = client.create_collection("life_memory")


def store_memory(text: str) -> None:
    """Store a memory with a stable content-based ID (deduplicates identical messages)."""
    stable_id = hashlib.md5(text.encode()).hexdigest()

    # Avoid duplicate IDs — upsert only if not already present
    existing = collection.get(ids=[stable_id])
    if not existing["documents"]:
        collection.add(
            documents=[text],
            ids=[stable_id],
        )


def retrieve_memory(query: str, n: int = 5) -> list[str]:
    """Return the top-n memories most semantically similar to query."""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n,
        )
        if results and results["documents"]:
            return results["documents"][0]
    except Exception:
        pass
    return []