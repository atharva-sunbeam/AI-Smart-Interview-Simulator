"""
Embedding Generation Pipeline

Purpose:
Generate semantic embeddings from the knowledge base.

Model:
sentence-transformers/all-MiniLM-L6-v2

Output:
datasets/processed/chunk_embeddings.pkl
"""

import csv
import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "processed" /
    "knowledge_base.csv"
)

EMBEDDING_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "processed" /
    "chunk_embeddings.pkl"
)


def load_knowledge_base():
    """
    Load knowledge base records.
    """

    with open(
        KNOWLEDGE_BASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        records = list(reader)

    return records


def generate_embeddings(records):
    """
    Generate embeddings for knowledge base content.
    """

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    contents = [
        record["content"]
        for record in records
    ]

    vectors = model.encode(
        contents,
        show_progress_bar=True
    )

    embeddings = []

    for record, vector in zip(
        records,
        vectors
    ):

        embeddings.append({
            "chunk_id":
                record["chunk_id"],

            "content":
                record["content"],

            "metadata": {
                "document_id":
                    record.get(
                        "document_id",
                        ""
                    ),

                "source_type":
                    record.get(
                        "source_type",
                        ""
                    ),

                "domain":
                    record.get(
                        "domain",
                        ""
                    ),

                "topic":
                    record.get(
                        "topic",
                        ""
                    )
            },

            "embedding":
                vector.tolist()
        })

    return embeddings


def get_embedding_dimension():
    """
    Return embedding dimension.
    """

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model.get_embedding_dimension()


def save_embeddings(
    embeddings
):
    """
    Save embeddings to disk.
    """

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
        f"Embedding Dimension: "
        f"{get_embedding_dimension()}"
    )

    print(
        f"Saved embeddings to:\n"
        f"{EMBEDDING_FILE}"
    )


if __name__ == "__main__":
    main()