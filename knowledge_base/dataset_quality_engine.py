"""
Dataset Quality Engine

Purpose:
Clean and score collected datasets before
building the knowledge base.

Pipeline:

Raw Dataset
      ↓
HTML Cleaning
      ↓
Quality Filtering
      ↓
Quality Scoring
      ↓
Processed Dataset
"""

import html
import re


class DatasetQualityEngine:
    """
    Dataset quality assessment and filtering.
    """

    def __init__(
        self,
        min_question_length: int = 15,
        min_answer_length: int = 50,
        min_stackoverflow_score: int = 5,
    ):
        self.min_question_length = min_question_length
        self.min_answer_length = min_answer_length
        self.min_stackoverflow_score = min_stackoverflow_score

    def remove_short_answers(
        self,
        records,
    ):
        """
        Remove records having very short answers.
        """

        return [
            record
            for record in records
            if len(
                record.get(
                    "answer",
                    "",
                ).strip()
            ) >= self.min_answer_length
        ]

    def remove_low_score_so_questions(
        self,
        records,
    ):
        """
        Remove low-quality Stack Overflow questions.
        """

        filtered = []

        for record in records:

            score = int(
                record.get(
                    "score",
                    0,
                )
            )

            if score >= self.min_stackoverflow_score:
                filtered.append(record)

        return filtered

    def remove_html(
        self,
        text: str,
    ):
        """
        Remove HTML tags and HTML entities.
        """

        text = html.unescape(text)

        text = re.sub(
            r"<[^>]+>",
            "",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def assign_quality_score(
        self,
        record,
    ):
        """
        Assign quality score (0-100).
        """

        score = 0

        question = record.get(
            "question",
            "",
        )

        answer = record.get(
            "answer",
            "",
        )

        so_score = int(
            record.get(
                "score",
                0,
            )
        )

        accepted = record.get(
            "accepted_answer",
            "",
        )

        # Question Length (25)
        score += min(
            len(question) / 80,
            1,
        ) * 25

        # Answer Length (35)
        score += min(
            len(answer) / 500,
            1,
        ) * 35

        # StackOverflow Score (30)
        score += min(
            so_score / 100,
            1,
        ) * 30

        # Accepted Answer (10)
        if accepted:
            score += 10

        return round(score, 2)

    def filter_records(
        self,
        records,
        minimum_quality: float = 60,
    ):
        """
        Clean and filter dataset.
        """

        cleaned_records = []

        for record in records:

            record["question"] = self.remove_html(
                record.get(
                    "question",
                    "",
                )
            )

            record["answer"] = self.remove_html(
                record.get(
                    "answer",
                    "",
                )
            )

            quality = self.assign_quality_score(
                record
            )

            record["quality_score"] = quality

            if quality >= minimum_quality:
                cleaned_records.append(
                    record
                )

        cleaned_records = (
            self.remove_short_answers(
                cleaned_records
            )
        )

        cleaned_records = (
            self.remove_low_score_so_questions(
                cleaned_records
            )
        )

        return cleaned_records


if __name__ == "__main__":

    engine = DatasetQualityEngine()

    sample = {
        "question":
            "<b>What is Python?</b>",

        "answer":
            "<p>Python is a high-level interpreted programming language used for web development, automation, data science, artificial intelligence, scripting, and many other applications.</p>",

        "score":
            120,

        "accepted_answer":
            "12345",
    }

    sample["question"] = engine.remove_html(
        sample["question"]
    )

    sample["answer"] = engine.remove_html(
        sample["answer"]
    )

    sample["quality_score"] = (
        engine.assign_quality_score(
            sample
        )
    )

    print(sample)