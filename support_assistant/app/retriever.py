import chromadb
from pathlib import Path
from app.embeddings import load_embedding_model

# Load once
embedding_model = load_embedding_model()

# Connect once
# Project root = /app
BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DB_PATH = BASE_DIR / "chroma_db"

# Load embedding model once
embedding_model = load_embedding_model()

# Connect to the correct ChromaDB
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = chroma_client.get_or_create_collection(
    name="zepto_collection",metadata={"hnsw:space": "cosine"}     # cosine similarity
)

def retrieve(question,top_k=3):

    # embed the question with the same model
    query_embedding = embedding_model.encode(question).tolist()

    # get the top 3 embeddings from chroma db collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return {
        "documents": results["documents"][0],
        "ids":results["ids"][0]
    }

if __name__ == "__main__":
    docs = retrieve("How do I cancel my order?")

    for i, doc in enumerate(docs, 1):
        print(f"\nDocument {i}\n")
        print(doc[:200])