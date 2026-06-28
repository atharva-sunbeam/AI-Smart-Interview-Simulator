"""
Semantic Deduplication Engine

Purpose:
Remove semantically similar interview
questions collected from multiple sources.

Input:
datasets/cleaned/cleaned_qa.csv

Output:
datasets/cleaned/deduplicated_qa.csv
"""

from pathlib import Path

import pandas as pd
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# Optional future scalability
try:
    import faiss

    FAISS_AVAILABLE = True

except ImportError:

    FAISS_AVAILABLE = False


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

INPUT_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "cleaned" /
    "cleaned_qa.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "cleaned" /
    "deduplicated_qa.csv"
)


class SemanticDeduplicator:
    """
    Semantic deduplication engine.
    """

    def __init__(
        self,
        threshold=0.90
    ):

        self.threshold = threshold

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.dataset = None
        self.embeddings = None

        # Stores duplicate information
        self.duplicate_records = []

    def load_dataset(
        self,
        file_path=INPUT_FILE
    ):
        """
        Load dataset.
        """

        self.dataset = pd.read_csv(
            file_path
        )

        print(
            f"\nLoaded "
            f"{len(self.dataset)} records."
        )

        return self.dataset

    def generate_embeddings(self):
        """
        Generate sentence embeddings.
        """

        questions = (
            self.dataset["question"]
            .fillna("")
            .tolist()
        )

        self.embeddings = (
            self.model.encode(
                questions,
                show_progress_bar=True
            )
        )

        print(
            "\nEmbeddings generated successfully."
        )

        return self.embeddings

    def find_duplicates(self):
        """
        Find semantic duplicates.

        Uses:

        - FAISS if available
        - Otherwise cosine similarity matrix
        """

        duplicate_indices = set()

        total = len(
            self.embeddings
        )

        print(
            "\nFinding semantic duplicates..."
        )

        #
        # Future scalable implementation
        #
        if FAISS_AVAILABLE:

            print(
                "Using FAISS for similarity search."
            )

            vectors = np.array(
                self.embeddings
            ).astype("float32")

            dimension = vectors.shape[1]

            index = faiss.IndexFlatIP(
                dimension
            )

            faiss.normalize_L2(vectors)

            index.add(vectors)

            similarities, indices = (
                index.search(
                    vectors,
                    10
                )
            )

            for i in range(total):

                for sim, idx in zip(
                    similarities[i],
                    indices[i]
                ):

                    if idx == i:
                        continue

                    if sim >= self.threshold:

                        duplicate_indices.add(
                            idx
                        )

                        self.duplicate_records.append(
                            {
                                "question_1":
                                    self.dataset.iloc[i][
                                        "question"
                                    ],

                                "question_2":
                                    self.dataset.iloc[idx][
                                        "question"
                                    ],

                                "similarity":
                                    round(
                                        float(sim),
                                        4
                                    )
                            }
                        )

        else:

            print(
                "FAISS not available."
            )

            print(
                "Using cosine similarity matrix."
            )

            similarity_matrix = (
                cosine_similarity(
                    self.embeddings
                )
            )

            for i in range(total):

                if i in duplicate_indices:
                    continue

                for j in range(
                    i + 1,
                    total
                ):

                    if j in duplicate_indices:
                        continue

                    similarity = (
                        similarity_matrix[i][j]
                    )

                    if (
                        similarity >=
                        self.threshold
                    ):

                        duplicate_indices.add(
                            j
                        )

                        self.duplicate_records.append(
                            {
                                "question_1":
                                    self.dataset.iloc[i][
                                        "question"
                                    ],

                                "question_2":
                                    self.dataset.iloc[j][
                                        "question"
                                    ],

                                "similarity":
                                    round(
                                        float(
                                            similarity
                                        ),
                                        4
                                    )
                            }
                        )

        print(
            f"\nDetected "
            f"{len(duplicate_indices)} duplicates."
        )

        return duplicate_indices

    def remove_duplicates(self):
        """
        Remove semantic duplicates.
        """

        duplicate_indices = (
            self.find_duplicates()
        )

        cleaned_dataset = (
            self.dataset.drop(
                list(
                    duplicate_indices
                )
            )
            .reset_index(drop=True)
        )

        original_count = len(
            self.dataset
        )

        final_count = len(
            cleaned_dataset
        )

        removed = (
            original_count -
            final_count
        )

        reduction = (
            removed /
            original_count
        ) * 100

        print(
            "\nDeduplication Statistics"
        )

        print(
            f"Original Records: "
            f"{original_count}"
        )

        print(
            f"Duplicates Removed: "
            f"{removed}"
        )

        print(
            f"Final Records: "
            f"{final_count}"
        )

        print(
            f"Reduction: "
            f"{reduction:.2f}%"
        )

        return cleaned_dataset

    def save_clean_dataset(
        self,
        cleaned_dataset,
        output_path=OUTPUT_FILE
    ):
        """
        Save deduplicated dataset.
        """

        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cleaned_dataset.to_csv(
            output_path,
            index=False
        )

        print(
            "\nSaved clean dataset:"
        )

        print(output_path)

    def save_duplicate_report(
        self,
        output_path=
        PROJECT_ROOT /
        "datasets" /
        "processed" /
        "duplicate_report.csv"
    ):
        """
        Save duplicate similarity report.
        """

        if not self.duplicate_records:

            print(
                "\nNo duplicates found."
            )

            return

        report = pd.DataFrame(
            self.duplicate_records
        )

        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        report.to_csv(
            output_path,
            index=False
        )

        print(
            "\nDuplicate report saved:"
        )

        print(output_path)


def main():

    deduplicator = (
        SemanticDeduplicator()
    )

    deduplicator.load_dataset()

    deduplicator.generate_embeddings()

    cleaned_dataset = (
        deduplicator.remove_duplicates()
    )

    deduplicator.save_clean_dataset(
        cleaned_dataset
    )

    deduplicator.save_duplicate_report()


if __name__ == "__main__":
    main()