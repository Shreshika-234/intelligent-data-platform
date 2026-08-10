from fastapi import FastAPI
from app.schemas import RequestSchema, ResponseSchema
from app.graph import graph
from app.embeddings import store_embeddings
import chromadb
from pathlib import Path

app = FastAPI()

def initialize_chromadb():

    BASE_DIR = Path(__file__).resolve().parent

    CHROMA_DB_PATH = BASE_DIR / "chroma_db"

    # Connect to the correct ChromaDB
    chroma_client = chromadb.PersistentClient(
        path=str(CHROMA_DB_PATH)
    )

    collection = chroma_client.get_or_create_collection(
        name="zepto_collection"
    )

    if collection.count() == 0:
        print("ChromaDB is empty. Running ingestion and embedding...")
        store_embeddings()
    else:
        print(f"ChromaDB already initialized. Count: {collection.count()}")


initialize_chromadb()


@app.get("/")
def home():
    return {"message": "Support Assistant is running"}

@app.post("/ask",response_model=ResponseSchema)
def support_agent(question:RequestSchema):
    result = graph.invoke({
        "question":question.question
    })

    return result

