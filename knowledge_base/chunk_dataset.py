"""
Dataset Chunking Pipeline

Purpose:
Convert cleaned interview datasets into chunks
for future knowledge base generation and embeddings.
"""

from pathlib import Path

CLEAN_DATASET = Path(
"datasets/cleaned/python_questions_cleaned.txt"
)

CHUNK_DATASET = Path(
"datasets/chunks/python_chunks.txt"
)

def load_clean_dataset():

# Load cleaned dataset.

    with open(
        CLEAN_DATASET,
        "r",
        encoding="utf-8"
    ) as file:
        entries = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return entries


def create_chunks(
entries,
chunk_size=5
):

# Create chunks from cleaned entries.


# Current Version:
# Fixed-size chunking.

# Future Version:
# Recursive chunking.


    chunks = []

    for index in range(
        0,
        len(entries),
        chunk_size
    ):
        chunk = entries[
            index:index + chunk_size
        ]

        chunks.append(
            "\n".join(chunk)
        )

    return chunks


def save_chunks(chunks):

# Save chunks to output file.

    CHUNK_DATASET.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CHUNK_DATASET,
        "w",
        encoding="utf-8"
    ) as file:

        for chunk in chunks:
            file.write(chunk)
            file.write(
                "\n\n=== CHUNK ===\n\n"
            )


def main():
    entries = load_clean_dataset()


    chunks = create_chunks(
        entries
    )

    save_chunks(
        chunks
    )

    print(
        f"Total Records: {len(entries)}"
    )

    print(
        f"Total Chunks: {len(chunks)}"
    )

    print(
        f"Saved chunks to "
        f"{CHUNK_DATASET}"
    )

if __name__ == "__main__":
    main()
