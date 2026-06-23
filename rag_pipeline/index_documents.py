"""
Document Indexing Pipeline

Purpose:
Load embeddings and index them into ChromaDB.

Pipeline:

Embeddings
      ↓
Prepare Documents
      ↓
ChromaDB Collection
"""

import pickle
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EMBEDDING_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "processed" /
    "chunk_embeddings.pkl"
)

CHROMA_DB_PATH = (
    PROJECT_ROOT /
    "chroma_db"
)

COLLECTION_NAME = (
    "interview_knowledge_base"
)


class DocumentIndexer:

    def __init__(self):

        self.client = (
            chromadb.PersistentClient(
                path=str(CHROMA_DB_PATH)
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )

    def load_embeddings(self):
        """
        Load serialized embeddings.
        """

        with open(
            EMBEDDING_FILE,
            "rb"
        ) as file:

            embeddings = pickle.load(
                file
            )

        return embeddings

    def prepare_documents(
        self,
        embeddings
    ):
        """
        Prepare documents for ChromaDB.
        """

        ids = []
        documents = []
        metadatas = []
        vectors = []

        for record in embeddings:

            ids.append(
                record["chunk_id"]
            )

            documents.append(
                record["content"]
            )

            metadatas.append(
                record["metadata"]
            )

            vectors.append(
                record["embedding"]
            )

        return (
            ids,
            documents,
            metadatas,
            vectors
        )

    def index_documents(
        self,
        ids,
        documents,
        metadatas,
        vectors
    ):
        """
        Insert documents into ChromaDB.
        """

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=vectors
        )

        print(
            f"Indexed "
            f"{len(ids)} "
            f"documents into ChromaDB."
        )


def main():

    indexer = DocumentIndexer()

    embeddings = (
        indexer.load_embeddings()
    )

    print(
        f"Loaded "
        f"{len(embeddings)} "
        f"embeddings."
    )

    (
        ids,
        documents,
        metadatas,
        vectors
    ) = indexer.prepare_documents(
        embeddings
    )

    indexer.index_documents(
        ids,
        documents,
        metadatas,
        vectors
    )

    print(
        "\nIndexing completed."
    )


if __name__ == "__main__":
    main()