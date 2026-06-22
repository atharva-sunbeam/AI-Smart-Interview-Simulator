import csv
from pathlib import Path

class KnowledgeBaseBuilder:
    """
    Builds the final knowledge base by combining
    chunk content and metadata records.
    """


    def load_chunks(self, chunk_file: str):
        chunks = []

        with open(chunk_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            chunks = list(reader)

        return chunks

    def load_metadata(self, metadata_file: str):
        metadata = []

        with open(metadata_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            metadata = list(reader)

        return metadata

    def merge_records(self, chunks, metadata):
        metadata_lookup = {
            record["chunk_id"]: record
            for record in metadata
        }

        knowledge_base = []

        for chunk in chunks:
            chunk_id = chunk["chunk_id"]

            if chunk_id in metadata_lookup:
                merged_record = {
                    "chunk_id": chunk_id,
                    "document_id": metadata_lookup[chunk_id]["document_id"],
                    "topic": metadata_lookup[chunk_id]["topic"],
                    "content": chunk["content"],
                }

                knowledge_base.append(merged_record)

        return knowledge_base

    def save_knowledge_base(
        self,
        records,
        output_file="datasets/processed/knowledge_base.csv",
    ):
        if not records:
            return

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "chunk_id",
                    "document_id",
                    "topic",
                    "content",
                ],
            )

            writer.writeheader()
            writer.writerows(records)

