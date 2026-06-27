"""
Knowledge Base Builder

Purpose:
Create knowledge_base.csv from chunk data.
"""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHUNK_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "chunks" /
    "python_chunks.txt"
)

KNOWLEDGE_BASE_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "processed" /
    "knowledge_base.csv"
)


class KnowledgeBaseBuilder:
    """
    Builds the final knowledge base.
    """

    def load_chunks(self):

        print("Reading chunk file...")

        with open(
            CHUNK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        raw_chunks = [
            chunk.strip()
            for chunk in content.split(
                "=== CHUNK ==="
            )
            if chunk.strip()
        ]

        chunks = []

        for index, chunk in enumerate(
            raw_chunks,
            start=1
        ):

            chunks.append(
                {
                    "chunk_id":
                        f"CHUNK{index:06d}",

                    "document_id":
                        f"DOC{index:06d}",

                    "source_type":
                        "interview_question",

                    "domain":
                        "Python",

                    "topic":
                        "General",

                    "content":
                        chunk
                }
            )

        return chunks

    def merge_records(
        self,
        chunks,
        metadata
    ):
        """
        Merge chunks and metadata.
        """

        metadata_lookup = {
            record["chunk_id"]: record
            for record in metadata
        }

        merged_records = []

        for chunk in chunks:

            chunk_id = chunk["chunk_id"]

            if chunk_id in metadata_lookup:

                merged_records.append(
                    {
                        "chunk_id": chunk_id,

                        "document_id":
                            metadata_lookup[
                                chunk_id
                            ].get(
                                "document_id",
                                "UNKNOWN"
                            ),

                        "topic":
                            metadata_lookup[
                                chunk_id
                            ].get(
                                "topic",
                                "General"
                            ),

                        "content":
                            chunk["content"],
                    }
                )

        return merged_records

    def save_knowledge_base(
        self,
        records
    ):

        KNOWLEDGE_BASE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            KNOWLEDGE_BASE_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "chunk_id",
                    "document_id",
                    "source_type",
                    "domain",
                    "topic",
                    "content"
                ]
            )

            writer.writeheader()

            writer.writerows(
                records
            )


def main():

    print(
        "\nStarting Knowledge Base Builder...\n"
    )

    builder = KnowledgeBaseBuilder()

    chunks = builder.load_chunks()

    print(
        f"Loaded {len(chunks)} chunks"
    )

    builder.save_knowledge_base(
        chunks
    )

    print(
        "\nKnowledge Base created successfully."
    )

    print(
        f"\nSaved to:\n{KNOWLEDGE_BASE_FILE}"
    )


if __name__ == "__main__":
    main()