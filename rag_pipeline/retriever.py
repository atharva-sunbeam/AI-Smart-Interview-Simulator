"""
Retriever Engine

Purpose:
Retrieve the most relevant chunks from the
vector database based on user query.

Pipeline:

User Query
      ↓
Embedding Generation
      ↓
Vector Similarity Search
      ↓
Top K Results
"""

import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EMBEDDING_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "processed" /
    "chunk_embeddings.pkl"
)


class Retriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.embeddings = (
            self.load_vector_database()
        )

    def load_vector_database(self):
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

    def retrieve_context(
        self,
        query,
        top_k=3
    ):
        """
        Retrieve top-k relevant chunks.
        """

        query_embedding = (
            self.model.encode(query)
        )

        similarities = []

        for record in self.embeddings:

            similarity = (
                cosine_similarity(
                    [query_embedding],
                    [record["embedding"]]
                )[0][0]
            )

            similarities.append(
                (
                    similarity,
                    record
                )
            )

        similarities.sort(
            key=lambda x: x[0],
            reverse=True
        )

        top_results = (
            similarities[:top_k]
        )

        return [
            result[1]
            for result in top_results
        ]

    def format_context(
        self,
        retrieved_chunks
    ):
        """
        Format retrieved chunks for LLM.
        """

        context = []

        for chunk in retrieved_chunks:

            context.append(
                chunk["content"]
            )

        return "\n\n".join(context)


def main():

    retriever = Retriever()

    query = (
        "Explain Python decorators"
    )

    results = (
        retriever.retrieve_context(
            query=query,
            top_k=3
        )
    )

    print(
        "\nRetrieved Chunks:\n"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Result {index}: "
            f"{result['chunk_id']}"
        )

    print(
        "\nFormatted Context:\n"
    )

    print(
        retriever.format_context(
            results
        )
    )


if __name__ == "__main__":
    main()