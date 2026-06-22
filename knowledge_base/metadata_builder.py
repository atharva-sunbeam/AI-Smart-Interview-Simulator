import csv
from pathlib import Path

class MetadataBuilder:
    """
    Builds metadata records for knowledge-base chunks.
    """


    def generate_chunk_id(self, index: int) -> str:
        return f"CHUNK{index:06d}"

    def generate_document_id(self, index: int) -> str:
        return f"DOC{index:06d}"

    def build_metadata_record(
        self,
        chunk_id: str,
        document_id: str,
        source_type: str,
        topic: str,
        content: str,
    ) -> dict:
        return {
            "chunk_id": chunk_id,
            "document_id": document_id,
            "source_type": source_type,
            "topic": topic,
            "content": content,
        }

    def save_metadata(
        self,
        records: list,
        output_file: str = "datasets/processed/chunk_metadata.csv",
    ) -> None:
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
                    "source_type",
                    "topic",
                    "content",
                ],
            )

            writer.writeheader()
            writer.writerows(records)
