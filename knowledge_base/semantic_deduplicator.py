"""
Semantic Deduplication Engine

Purpose:
Remove semantically similar interview questions
collected from multiple sources.

Input:
datasets/cleaned/cleaned_qa.csv

Output:
datasets/cleaned/deduplicated_qa.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

from sentence_transformers import (
    SentenceTransformer,
)

from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from sklearn.preprocessing import (
    normalize,
)

try:
    import faiss

    FAISS_AVAILABLE = True

except ImportError:

    FAISS_AVAILABLE = False


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

INPUT_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "cleaned"
    / "cleaned_qa.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "cleaned"
    / "deduplicated_qa.csv"
)

DUPLICATE_REPORT = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "duplicate_report.csv"
)


SOURCE_PRIORITY = {
    "StackOverflow": 5,
    "GeeksforGeeks": 4,
    "InterviewBit": 3,
    "GitHub": 2,
    "Blog": 1,
}


class SemanticDeduplicator:
    """
    Semantic Deduplication Engine.
    """

    def __init__(
        self,
        threshold=0.90,
        batch_size=1000,
    ):

        self.threshold = threshold
        self.batch_size = batch_size

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.dataset = None
        self.embeddings = None

        self.duplicate_records = []

    def load_dataset(
        self,
        file_path=INPUT_FILE,
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
        Generate and normalize embeddings.
        """

        questions = (
            self.dataset["question"]
            .fillna("")
            .tolist()
        )

        self.embeddings = (
            self.model.encode(
                questions,
                show_progress_bar=True,
            )
        )

        self.embeddings = normalize(
            self.embeddings
        )

        print(
            "\nEmbeddings generated "
            "and normalized."
        )

        return self.embeddings

    def choose_best_record(
        self,
        index1,
        index2,
    ):
        """
        Decide which duplicate record to keep.

        Preference order:

        1. Source priority
        2. Longer answer
        """

        row1 = self.dataset.iloc[index1]
        row2 = self.dataset.iloc[index2]

        source1 = row1.get(
            "source",
            "Blog",
        )

        source2 = row2.get(
            "source",
            "Blog",
        )

        priority1 = SOURCE_PRIORITY.get(
            source1,
            0,
        )

        priority2 = SOURCE_PRIORITY.get(
            source2,
            0,
        )

        if priority1 > priority2:

            return index1

        if priority2 > priority1:

            return index2

        answer1 = str(
            row1.get(
                "answer",
                "",
            )
        )

        answer2 = str(
            row2.get(
                "answer",
                "",
            )
        )

        if len(answer1) >= len(answer2):

            return index1

        return index2

    def find_duplicates_faiss(self):
        """
        Duplicate detection using FAISS.
        """

        print(
            "\nUsing FAISS search..."
        )

        vectors = np.array(
            self.embeddings
        ).astype("float32")

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(vectors)

        similarities, indices = (
            index.search(
                vectors,
                10,
            )
        )

        duplicate_indices = set()

        for i in range(
            len(vectors)
        ):

            for sim, idx in zip(
                similarities[i],
                indices[i],
            ):

                if idx == i:

                    continue

                if sim < self.threshold:

                    continue

                keep = self.choose_best_record(
                    i,
                    idx,
                )

                remove = (
                    idx
                    if keep == i
                    else i
                )

                duplicate_indices.add(
                    remove
                )

                self.duplicate_records.append(
                    {
                        "question_1":
                            self.dataset.iloc[
                                i
                            ][
                                "question"
                            ],

                        "question_2":
                            self.dataset.iloc[
                                idx
                            ][
                                "question"
                            ],

                        "similarity":
                            round(
                                float(sim),
                                4,
                            ),

                        "kept_record":
                            keep,

                        "removed_record":
                            remove,
                    }
                )

        return duplicate_indices

    def find_duplicates_batch(
        self,
    ):
        """
        Memory-efficient batch similarity.
        """

        print(
            "\nUsing batch cosine similarity..."
        )

        duplicate_indices = set()

        total = len(
            self.embeddings
        )

        for start in range(
            0,
            total,
            self.batch_size,
        ):

            end = min(
                start +
                self.batch_size,
                total,
            )

            batch = (
                self.embeddings[
                    start:end
                ]
            )

            similarities = (
                cosine_similarity(
                    batch,
                    self.embeddings,
                )
            )

            for i in range(
                end - start
            ):

                global_i = (
                    start + i
                )

                if (
                    global_i
                    in duplicate_indices
                ):
                    continue

                for j in range(
                    total
                ):

                    if j <= global_i:

                        continue

                    if (
                        j
                        in duplicate_indices
                    ):
                        continue

                    similarity = (
                        similarities[i][j]
                    )

                    if (
                        similarity
                        >= self.threshold
                    ):

                        keep = (
                            self.choose_best_record(
                                global_i,
                                j,
                            )
                        )

                        remove = (
                            j
                            if keep
                            == global_i
                            else global_i
                        )

                        duplicate_indices.add(
                            remove
                        )

                        self.duplicate_records.append(
                            {
                                "question_1":
                                    self.dataset.iloc[
                                        global_i
                                    ][
                                        "question"
                                    ],

                                "question_2":
                                    self.dataset.iloc[
                                        j
                                    ][
                                        "question"
                                    ],

                                "similarity":
                                    round(
                                        float(
                                            similarity
                                        ),
                                        4,
                                    ),

                                "kept_record":
                                    keep,

                                "removed_record":
                                    remove,
                            }
                        )

        return duplicate_indices

    def find_duplicates(self):
        """
        Select best strategy.
        """

        total = len(
            self.embeddings
        )

        print(
            "\nFinding duplicates..."
        )

        if (
            FAISS_AVAILABLE
            and total > 20000
        ):

            return (
                self.find_duplicates_faiss()
            )

        return (
            self.find_duplicates_batch()
        )

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
            .reset_index(
                drop=True
            )
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

        print(
            f"Duplicate Pairs: "
            f"{len(self.duplicate_records)}"
        )

        print(
            f"Threshold Used: "
            f"{self.threshold}"
        )

        return cleaned_dataset

    def save_clean_dataset(
        self,
        cleaned_dataset,
        output_path=OUTPUT_FILE,
    ):
        """
        Save cleaned dataset.
        """

        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cleaned_dataset.to_csv(
            output_path,
            index=False,
        )

        print(
            f"\nSaved clean dataset:"
        )

        print(output_path)

    def save_duplicate_report(
        self,
        output_path=DUPLICATE_REPORT,
    ):
        """
        Save duplicate report.
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
            exist_ok=True,
        )

        report.to_csv(
            output_path,
            index=False,
        )

        print(
            "\nSaved duplicate report:"
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