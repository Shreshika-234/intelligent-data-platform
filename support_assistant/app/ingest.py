from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"


def ingest_documents():

    documents = []

    for filename in sorted(os.listdir(DOCS_DIR)):

        file_path = DOCS_DIR / filename

        with open(file_path, "r", encoding="utf-8") as file:

            documents.append({
                "id": filename.replace(".txt", ""),
                "text": file.read()
            })

    return documents