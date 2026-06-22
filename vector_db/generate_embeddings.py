"""
Embedding Generation Pipeline

Purpose:
Generate embeddings from the knowledge base
for future storage in ChromaDB.

Model:
sentence-transformers/all-MiniLM-L6-v2

Output:
datasets/processed/chunk_embeddings.pkl
"""

import csv
import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE_FILE = Path(
"datasets/processed/knowledge_base.csv"
)

EMBEDDING_FILE = Path(
"datasets/processed/chunk_embeddings.pkl"
)

def load_knowledge_base():

# Load knowledge base records.

    records = []

    with open(
        KNOWLEDGE_BASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        records = list(reader)

    return records

def generate_embeddings(records):

# Generate embeddings for chunk content.

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = []

    for record in records:

        embedding = model.encode(
            record["content"]
        )

        embeddings.append({
            "chunk_id": record["chunk_id"],
            "embedding": embedding
        })

    return embeddings

def save_embeddings(embeddings):

# Save embeddings to disk.

    EMBEDDING_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        EMBEDDING_FILE,
        "wb"
    ) as file:

        pickle.dump(
            embeddings,
            file
        )


def main():
    records = load_knowledge_base()


    embeddings = generate_embeddings(
        records
    )

    save_embeddings(
        embeddings
    )

    print(
        f"Knowledge Base Records: "
        f"{len(records)}"
    )

    print(
        f"Generated Embeddings: "
        f"{len(embeddings)}"
    )

    print(
        f"Saved embeddings to "
        f"{EMBEDDING_FILE}"
    )


if __name__ == "__main__":
    main()
