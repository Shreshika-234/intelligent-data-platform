# 🚀 Intelligent Data Platform

An end-to-end **Data Engineering, Data Analytics, and Generative AI** capstone project that demonstrates how different data and AI technologies can be combined to build practical data-driven applications.

The project is organized into three independent modules:

- **📊 Data Pipeline** — Data collection, processing, and database storage.
- **📈 Analytics** — Data analysis and machine learning.
- **🤖 Support Assistant** — AI-powered question answering using Retrieval-Augmented Generation (RAG).

Each module contains its own detailed `README.md` with implementation details, execution steps, and results.

---

# 📂 Repository Structure

```text
intelligent-data-platform/
│
├── README.md
│
├── data_pipeline/
│   ├── scraper.py
│   ├── clean.py
│   ├── database.ipynb
│   ├── queries.py
│   ├── requirements.txt
│   ├── README.md
│   └── data/
│       ├── raw_books.csv
│       ├── clean_books.csv
│       ├── books.db
│       └── query_results.txt
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── clean_titanic.csv
│   ├── best_random_forest_pipeline.pkl
│   └── README.md
│
└── support_assistant/
    ├── app/
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
    ├── main.py
    ├── Dockerfile
    ├── requirements.txt
    └── README.md
```

---

# 🚀 Project Modules

## 1️⃣ 📊 Data Pipeline

The Data Pipeline module demonstrates the data engineering lifecycle, starting from collecting raw data and progressing through data processing and database storage.

The module works with book data collected from an online source and produces structured datasets and a SQLite database for further analysis.

### 🛠️ Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- SQL

### 📁 Module

```text
data_pipeline/
```

For detailed implementation and execution instructions, see:

```text
data_pipeline/README.md
```

---

## 2️⃣ 📈 Analytics

The Analytics module demonstrates the data analytics and machine learning lifecycle using the Titanic dataset.

It covers the process of working with a real dataset, performing analysis, building predictive models, evaluating results, and saving the resulting model artifact.

### 🛠️ Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Joblib
- Jupyter Notebook

### 📁 Module

```text
analytics/
```

For detailed analysis, modeling, evaluation, and results, see:

```text
analytics/README.md
```

---

## 3️⃣ 🤖 Support Assistant

The Support Assistant is a Generative AI application designed to answer customer support questions using a knowledge base of support documents.

The application demonstrates a Retrieval-Augmented Generation (RAG) architecture with vector search, workflow orchestration, structured responses, and an API layer.

### 🛠️ Technologies

- Python
- Sentence Transformers
- ChromaDB
- LangGraph
- FastAPI
- Pydantic
- Groq
- Docker

### 📁 Module

```text
support_assistant/
```

For detailed implementation, RAG workflow, configuration, and execution instructions, see:

```text
support_assistant/README.md
```

---

# 🧰 Technology Stack

The project brings together technologies from several areas:

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Collection | Requests, BeautifulSoup |
| Data Processing | Pandas, NumPy |
| Database | SQLite, SQL |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Model Persistence | Joblib |
| Notebooks | Jupyter |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| AI Workflow | LangGraph |
| LLM | Groq |
| Backend API | FastAPI, Uvicorn |
| Data Validation | Pydantic |
| Containerization | Docker |
| Version Control | Git, GitHub |

---

# 🔄 High-Level Project Workflow

The project contains three complementary workflows rather than a single linear pipeline.

```text
                    🚀 INTELLIGENT DATA PLATFORM
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    📊 DATA PIPELINE      📈 ANALYTICS      🤖 SUPPORT ASSISTANT
          │                   │                   │
          ▼                   ▼                   ▼
   Data Collection       Data Analysis       Knowledge Base
          │                   │                   │
          ▼                   ▼                   ▼
   Data Processing      Machine Learning       AI / RAG
          │                   │                   │
          ▼                   ▼                   ▼
       SQLite              Results          Question Answering
```

Each module focuses on a different part of the modern data and AI ecosystem while remaining independently executable.

---

# ▶️ Running the Projects

Each module contains its own `requirements.txt` and detailed setup instructions.

---

## 📊 Data Pipeline

Navigate to:

```bash
cd data_pipeline
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Follow the detailed instructions in:

```text
data_pipeline/README.md
```

---

## 📈 Analytics

Navigate to:

```bash
cd analytics
```

Install the required dependencies and open the notebooks:

```text
01_eda.ipynb
02_modeling.ipynb
```

Detailed instructions are available in:

```text
analytics/README.md
```

---

## 🤖 Support Assistant

Navigate to:

```bash
cd support_assistant
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Follow the detailed setup instructions in:

```text
support_assistant/README.md
```

The Support Assistant can be run locally using FastAPI or using Docker.

---

# 🎓 Learning Outcomes

This capstone provides practical experience across multiple areas of modern software and data development.

### 📊 Data Engineering

- Data collection
- Data ingestion
- Data cleaning
- Data transformation
- Database storage
- SQL

### 📈 Data Analytics

- Exploratory data analysis
- Data visualization
- Data preprocessing
- Machine learning
- Model evaluation

### 🤖 Generative AI

- Document processing
- Text embeddings
- Vector databases
- Semantic retrieval
- Retrieval-Augmented Generation
- Prompt engineering
- LLM integration

### 🌐 Application Development

- FastAPI
- REST APIs
- Pydantic
- Workflow orchestration

### 🐳 Deployment

- Docker
- Environment configuration
- Persistent storage
- Git and GitHub

---

# 📋 Module Summary

| Module | Overview |
|---|---|
| **📊 Data Pipeline** | Collects and processes raw book data and stores it in a structured database. |
| **📈 Analytics** | Performs analysis and machine learning using the Titanic dataset. |
| **🤖 Support Assistant** | Provides AI-powered customer support using a RAG-based architecture. |

---

# 🎯 Project Goals

The main goals of this capstone are to demonstrate practical understanding of:

- Data Engineering
- Data Analytics
- Machine Learning
- Generative AI
- Vector Databases
- API Development
- Workflow Orchestration
- Containerization
- Software Development Practices

---

# 🏁 Conclusion

The **Intelligent Data Platform** brings together three different areas of modern technology:

```text
📊 Data Engineering
        +
📈 Data Analytics
        +
🤖 Generative AI
```

The project demonstrates the ability to work with data from its initial collection and processing stages through analytics and machine learning, while also building an AI-powered application using modern RAG and API technologies.

Detailed implementation and results for each module are documented in their respective module-level `README.md` files.