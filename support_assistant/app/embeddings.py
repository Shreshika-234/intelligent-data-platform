from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from app.ingest import ingest_documents


# support_assistant/
BASE_DIR = Path(__file__).resolve().parent.parent

# support_assistant/chroma_db/
CHROMA_DB_PATH = BASE_DIR / "chroma_db"


def load_embedding_model():
    """Load the embedding model."""
    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )


def generate_embeddings(embedding_model, documents):
    """Generate embeddings for the provided documents."""

    text_docs = [doc["text"] for doc in documents]
    ids = [doc["id"] for doc in documents]

    embeddings = embedding_model.encode(text_docs)

    return ids, text_docs, embeddings


def store_embeddings():
    """Store document embeddings in ChromaDB."""

    # 1. Ingest documents
    documents = ingest_documents()

    print(f"Loaded {len(documents)} documents")

    # 2. Load embedding model
    embedding_model = load_embedding_model()

    # 3. Generate embeddings
    ids, text_docs, embeddings = generate_embeddings(
        embedding_model,
        documents
    )

    print(f"Generated {len(embeddings)} embeddings")

    # 4. Connect to persistent ChromaDB
    chroma_client = chromadb.PersistentClient(
        path=str(CHROMA_DB_PATH)
    )

    # 5. Create/get collection
    collection = chroma_client.get_or_create_collection(
        name="zepto_collection",
        metadata={"hnsw:space": "cosine"}
    )

    # 6. Store embeddings
    collection.upsert(
        ids=ids,
        documents=text_docs,
        embeddings=embeddings.tolist()
    )

    print(f"Stored {collection.count()} documents in the collection")
    print(f"ChromaDB path: {CHROMA_DB_PATH}")

    return collection


if __name__ == "__main__":
    store_embeddings()