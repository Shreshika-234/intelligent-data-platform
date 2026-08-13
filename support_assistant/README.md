# Support Assistant

A small FastAPI-based GenAI support assistant for Zepto.

The application uses a local document corpus, Sentence Transformers for embeddings, ChromaDB for vector storage and retrieval, LangGraph for intent-based routing, Pydantic for structured output validation, and FastAPI as the API layer.

The required baseline runs fully offline using `MOCK_LLM=1`. A real Groq LLM integration is available as an optional extension using `MOCK_LLM=0`.

---

## Features

- FastAPI API exposed through `main.py`
- Document ingestion from `docs/`
- Local embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB persistent vector storage
- Top-3 cosine-similarity retrieval
- LangGraph state graph with conditional routing
- Deterministic mock LLM mode
- Optional Groq real-LLM mode
- Pydantic structured JSON response
- JSON validation and retry logic for real LLM responses
- Docker support

---

## Project Structure

```text
support_assistant/
│
├── app/
│   ├── __init__.py
│   ├── ingest.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── prompt.py
│   ├── schemas.py
│   ├── models.py
│   ├── nodes.py
│   └── graph.py
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── chroma_db/
│
├── main.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# Document Corpus

The application contains 8 Zepto policy documents:

| Document | Policy |
|---|---|
| `doc_01` | Delivery Policy |
| `doc_02` | Returns & Refunds |
| `doc_03` | Membership Tiers |
| `doc_04` | Order Tracking |
| `doc_05` | Order Cancellation Policy |
| `doc_06` | Damaged or Missing Items |
| `doc_07` | Gift Cards |
| `doc_08` | Customer Support Hours |

Each document is treated as one chunk because the documents are short.

---

# Architecture

The complete RAG pipeline is:

```text
                    User Question
                         |
                         v
                  +--------------+
                  |   FastAPI    |
                  |    /ask      |
                  +--------------+
                         |
                         v
                  +--------------+
                  |  LangGraph   |
                  |classify_intent|
                  +--------------+
                         |
                 +-------+-------+
                 |               |
                 v               v
          policy_question   general_question
                 |               |
                 v               v
      +---------------------+ +---------------+
      | retrieve_and_answer | | direct_answer |
      +---------------------+ +---------------+
                 |
                 v
          Query Embedding
                 |
                 v
             +--------+
             |ChromaDB|
             | Top-3  |
             +--------+
                 |
                 v
        Retrieved Context
                 |
                 v
          Answer Generation
                 |
                 v
        Pydantic Validation
                 |
                 v
          Structured JSON
```

---

# RAG Pipeline

## 1. Ingestion

Document ingestion is implemented in:

```text
app/ingest.py
```

The function:

```python
ingest_documents()
```

reads all documents from:

```text
docs/
```

Each document is converted into an object containing:

```python
{
    "id": "doc_05",
    "text": "Order Cancellation Policy: ..."
}
```

The filename is used as the document/chunk ID.

For example:

```text
doc_01.txt -> doc_01
doc_02.txt -> doc_02
...
doc_08.txt -> doc_08
```

Since the documents are short, each document is treated as one chunk.

---

# 2. Embedding

Embedding is implemented in:

```text
app/embeddings.py
```

The application uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model runs locally.

The flow is:

```text
Document text
      |
      v
all-MiniLM-L6-v2
      |
      v
Embedding vector
```

All 8 documents are embedded and stored in ChromaDB.

---

# 3. ChromaDB Storage

ChromaDB is used as the vector database.

The collection is:

```text
zepto_collection
```

The application uses cosine similarity.

The persistent database directory is:

```text
chroma_db/
```

The path is calculated using `pathlib`.

---

# 4. Retrieval

Retrieval is implemented in:

```text
app/retriever.py
```

The function is:

```python
retrieve(question, top_k=3)
```

The question is embedded using the same:

```text
all-MiniLM-L6-v2
```

model.

The query embedding is then sent to ChromaDB.

ChromaDB returns the top 3 most similar chunks.

The retriever returns:

```python
{
    "documents": [...],
    "ids": [...]
}
```

For example, for:

```text
How do I cancel my order?
```

the retrieval result can include:

```text
doc_05
doc_06
doc_02
```

with `doc_05` being the most relevant document.

---

# LangGraph

The LangGraph implementation is in:

```text
app/graph.py
```

The graph contains three nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

The graph routing is:

```text
START
  |
  v
classify_intent
  |
  +--------------------------+
  |                          |
  v                          v
policy_question        general_question
  |                          |
  v                          v
retrieve_and_answer     direct_answer
  |                          |
  +------------+-------------+
               |
               v
              END
```

The routing itself does not depend on `MOCK_LLM`.

Only the generation/classification steps inside the nodes branch on `MOCK_LLM`.

---

# Intent Classification

Intent classification is implemented in:

```text
app/nodes.py
```

The application supports:

```text
policy_question
general_question
```

## Mock Mode

When:

```text
MOCK_LLM=1
```

the application does not call an LLM for intent classification.

It uses the required keyword heuristic.

The keywords are:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

If any keyword occurs in the lowercased question:

```text
policy_question
```

is selected.

Otherwise:

```text
general_question
```

is selected.

Example:

```text
Question:
How do I cancel my order?

Intent:
policy_question
```

Example:

```text
Question:
Tell me a joke.

Intent:
general_question
```

---

# Mock LLM Mode

The default mode is:

```text
MOCK_LLM=1
```

or `MOCK_LLM` can be left unset.

This is the required graded baseline.

No LLM API call is made in this mode.

The mock logic is deterministic.

---

# Policy Question Generation

For a policy question, LangGraph routes the query to:

```text
retrieve_and_answer
```

Retrieval always happens, even in mock mode.

The top 3 chunks are retrieved from ChromaDB.

In mock mode, no LLM is used for final answer generation.

Instead, the application returns a deterministic response using the first approximately 200 characters of the most similar retrieved chunk.

Example:

```text
Based on the retrieved context:

Order Cancellation Policy: "Orders can be cancelled free of cost any time before the order status changes to 'Packed'...
```

The response also contains the retrieved document IDs as `sources`.

---

# General Question Generation

For a general question, LangGraph routes the query to:

```text
direct_answer
```

No retrieval is performed.

In mock mode, the fixed response is:

```text
I can only answer questions about Zepto policies right now.
```

The sources list is empty because no policy documents were retrieved.

---

# Structured Output

The final API response is validated using the Pydantic model:

```text
app/schemas.py
```

The response contains:

```json
{
  "answer": "string",
  "sources": [],
  "confidence": 1.0
}
```

The three fields are:

| Field | Type | Description |
|---|---|---|
| `answer` | string | Final answer |
| `sources` | list[string] | Retrieved document/chunk IDs |
| `confidence` | float | Confidence between 0 and 1 |

For policy questions, `sources` contains the retrieved document IDs.

For general questions:

```json
"sources": []
```

In mock mode:

```json
"confidence": 1.0
```

---

# Structured Prompt

The policy-answer prompt is implemented in:

```text
app/prompt.py
```

The prompt follows the required structure:

```text
Role
Context
Task
Format
Length
```

It also contains the negative constraint:

```text
Do not answer using information that is not present in the provided context.
```

The prompt also contains a few-shot example showing the expected answer format.

The structured prompt is used by the optional real-LLM path.

---

# Real LLM Mode

The real LLM path is optional.

Set:

```text
MOCK_LLM=0
```

and provide:

```text
GROQ_API_KEY=your_api_key
```

The current implementation uses:

```text
llama-3.1-8b-instant
```

through Groq.

In real LLM mode:

- Intent classification uses the LLM.
- Policy questions retrieve the top-3 documents and then use the LLM to generate the answer.
- General questions are answered directly by the LLM.
- The final JSON response is validated using Pydantic.

Embedding and ChromaDB retrieval remain local.

---

# JSON Validation and Retry

The raw real-LLM response is validated using:

```python
ResponseSchema.model_validate_json(raw_output)
```

If the LLM returns invalid JSON, the response is rejected.

The application retries up to 3 total attempts.

On validation failure, a corrective instruction is added:

```text
Your previous response was not valid JSON.

Return ONLY valid JSON matching the required schema.

Do not include any extra text.
```

If all 3 attempts fail, the application returns:

```json
{
  "answer": "ERROR: Failed to generate valid JSON.",
  "sources": [],
  "confidence": 0.0
}
```

---

# FastAPI

The FastAPI application is implemented in:

```text
main.py
```

The main endpoint is:

```text
POST /ask
```

Request:

```json
{
  "question": "How do I cancel my order?"
}
```

The request is passed to the LangGraph:

```python
result = graph.invoke({
    "question": question.question
})
```

The final response is returned using the Pydantic `ResponseSchema`.

---

# Running Locally

## Prerequisites

- Python 3.10+
- Virtual environment
- Internet connection for installing dependencies and downloading the embedding model initially

The LLM itself does not require network access when using `MOCK_LLM=1`.

---

## Install Dependencies

From the `support_assistant` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside `support_assistant/`.

For the required mock mode:

```text
MOCK_LLM=1
```

For the optional real LLM mode:

```text
MOCK_LLM=0
GROQ_API_KEY=your_groq_api_key
```

Example:

```text
MOCK_LLM=1
GROQ_API_KEY=your_groq_api_key
```

The Groq API key is not required when `MOCK_LLM=1`.

Never commit a real API key to the repository.

---

# Initialize / Re-ingest Documents

The documents can be embedded manually using:

```bash
python3 -m app.embeddings
```

This:

1. Loads the 8 documents.
2. Generates embeddings using `all-MiniLM-L6-v2`.
3. Stores the embeddings in ChromaDB.
4. Creates or updates the `zepto_collection`.

Example output:

```text
Loaded 8 documents
Generated 8 embeddings
Stored 8 documents in the collection
ChromaDB path: support_assistant/chroma_db
```

The database is stored in:

```text
support_assistant/chroma_db/
```

---

# Automatic First-Time Initialization

The FastAPI application also checks ChromaDB during startup.

If the collection is empty:

```text
ChromaDB is empty. Running ingestion and embedding...
Loaded 8 documents
Generated 8 embeddings
Stored 8 documents in the collection
```

If the collection already contains documents:

```text
ChromaDB already initialized. Count: 8
```

Therefore, the application can initialize the database automatically when starting with an empty ChromaDB.

---

# Run the API

Start the FastAPI application:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

The API is available at:

```text
http://localhost:7860
```

Swagger UI:

```text
http://localhost:7860/docs
```

---

# Example 1 — Policy Question

Request:

```json
{
  "question": "How do I cancel my order?"
}
```

This contains the keyword:

```text
cancel
```

Therefore:

```text
classify_intent
        |
        v
policy_question
        |
        v
retrieve_and_answer
```

With `MOCK_LLM=1`, an example response is:

```json
{
  "answer": "Based on the retrieved context:\n\nOrder Cancellation Policy: \"Orders can be cancelled free of cost any time before the order status changes to 'Packed', typically within the first 2 minutes...",
  "sources": [
    "doc_05",
    "doc_06",
    "doc_02"
  ],
  "confidence": 1
}
```

The exact answer text and retrieved source ordering may vary depending on the retrieval result.

---

# Example 2 — General Question

Request:

```json
{
  "question": "Tell me a joke."
}
```

This does not contain a policy keyword.

Therefore:

```text
classify_intent
        |
        v
general_question
        |
        v
direct_answer
```

With `MOCK_LLM=1`, the response is:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```

---

# Testing with curl

## Policy Question

```bash
curl -X POST "http://localhost:7860/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I cancel my order?"}'
```

## General Question

```bash
curl -X POST "http://localhost:7860/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me a joke."}'
```

---

# Docker

A Dockerfile is included for local containerization.

## Build

From the `support_assistant` directory:

```bash
docker build -t support-assistant .
```

## Run

```bash
docker run -d \
  --name support-assistant-container \
  --env-file .env \
  -p 7860:7860 \
  -v "$(pwd)/chroma_db:/app/chroma_db" \
  support-assistant
```

The application will be available at:

```text
http://localhost:7860
```

Swagger:

```text
http://localhost:7860/docs
```

The bind mount keeps the ChromaDB files in:

```text
support_assistant/chroma_db/
```

on the local machine.

This allows the ChromaDB created inside the container to persist to the host machine.

---

# Docker Verification

Check the container:

```bash
docker ps -a
```

Check application logs:

```bash
docker logs -f support-assistant-container
```

Expected first-time initialization logs include:

```text
ChromaDB is empty. Running ingestion and embedding...
Loaded 8 documents
Generated 8 embeddings
Stored 8 documents in the collection
```

After initialization, the API starts with Uvicorn:

```text
Uvicorn running on http://0.0.0.0:7860
```

On subsequent container starts, if the same host `chroma_db` directory is mounted and already contains the collection, the application should detect the existing documents instead of ingesting them again.

---

# Docker API Test

```bash
curl -X POST "http://localhost:7860/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I cancel my order?"}'
```

---

# MOCK_LLM Summary

| Stage | `MOCK_LLM=1` | `MOCK_LLM=0` |
|-------|--------------|--------------|
| Intent classification | Keyword heuristic | Groq LLM |
| Query embedding | Local model | Local model |
| ChromaDB retrieval | Real retrieval | Real retrieval |
| Policy answer generation | Deterministic mock | Groq LLM |
| General answer generation | Fixed canned response | Groq LLM |
| Pydantic validation | Deterministic schema population | Raw LLM JSON validation |
| Retry logic | Not required | Up to 3 attempts |

The important point is that the retrieval stage is always performed for policy questions.

Only the classification/generation steps change based on `MOCK_LLM`.

---

# End-to-End Flow

```text
1. User sends question
             |
             v
2. FastAPI /ask
             |
             v
3. LangGraph classify_intent
             |
       +-----+-----+
       |           |
       v           v
 policy        general
       |           |
       v           v
 retrieval     direct answer
       |
       v
4. Embed query using all-MiniLM-L6-v2
       |
       v
5. Query ChromaDB
       |
       v
6. Retrieve top-3 chunks
       |
       v
7. Generate answer
       |
       +---- MOCK_LLM=1 --> deterministic response
       |
       +---- MOCK_LLM=0 --> Groq LLM
       |
       v
8. Validate ResponseSchema
       |
       v
9. Return JSON response
```

---

# Files and Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | FastAPI application and ChromaDB initialization |
| `app/ingest.py` | Reads the 8 policy documents |
| `app/embeddings.py` | Generates and stores document embeddings |
| `app/retriever.py` | Embeds queries and retrieves top-3 chunks |
| `app/prompt.py` | Structured RAG and general-answer prompts |
| `app/schemas.py` | Pydantic request/response schemas |
| `app/models.py` | LangGraph state definition |
| `app/nodes.py` | Intent classification, retrieval and answer generation |
| `app/graph.py` | LangGraph StateGraph and conditional routing |
| `docs/` | Zepto policy corpus |
| `chroma_db/` | Persistent ChromaDB storage |
| `Dockerfile` | Container configuration |