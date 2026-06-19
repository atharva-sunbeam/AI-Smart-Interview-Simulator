"""
Dataset Cleaning Pipeline

Purpose:
Clean raw interview question datasets before
chunking and knowledge base generation.
"""

from pathlib import Path

RAW_DATASET = Path(
"datasets/raw/python_questions.txt"
)

CLEANED_DATASET = Path(
"datasets/cleaned/python_questions_cleaned.txt"
)

def remove_empty_lines(entries):
    return [
    entry.strip()
    for entry in entries
    if entry.strip()
    ]

def remove_duplicates(entries):
    return list(
    dict.fromkeys(entries)
    )

def remove_short_entries(
entries,
min_length=10
):
    return [
    entry
    for entry in entries
    if len(entry) >= min_length
    ]

def main():
    with open(
    RAW_DATASET,
    "r",
    encoding="utf-8"
    ) as file:
        entries = file.readlines()


    entries = remove_empty_lines(
        entries
    )

    entries = remove_duplicates(
        entries
    )

    entries = remove_short_entries(
        entries
    )

    CLEANED_DATASET.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CLEANED_DATASET,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            "\n".join(entries)
        )

    print(
        f"Raw Records: {len(open(RAW_DATASET, encoding='utf-8').readlines())}"
    )

    print(
        f"Clean Records: {len(entries)}"
    )

    print(
        f"Saved cleaned dataset to "
        f"{CLEANED_DATASET}"
    )


if __name__ == "__main__":
    main()
