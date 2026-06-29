"""
Dataset Quality Engine

Purpose:
Clean, score, and filter collected datasets before
building the RAG knowledge base.

Pipeline:

Raw Dataset
        ↓
HTML Cleaning
        ↓
Question Filtering
        ↓
Answer Filtering
        ↓
Quality Scoring
        ↓
Dataset Filtering
        ↓
Knowledge Base
"""

import html
import re


class DatasetQualityEngine:
    """
    Dataset quality assessment engine.
    """

    TECH_KEYWORDS = {
        "python",
        "java",
        "sql",
        "database",
        "query",
        "class",
        "object",
        "function",
        "method",
        "inheritance",
        "polymorphism",
        "encapsulation",
        "abstraction",
        "decorator",
        "generator",
        "yield",
        "iterator",
        "spark",
        "kafka",
        "airflow",
        "etl",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "api",
        "rest",
        "json",
        "microservices",
        "tensorflow",
        "pytorch",
        "machine",
        "learning",
        "deep",
        "model",
        "pandas",
        "numpy",
        "scikit-learn",
    }

    def __init__(
        self,
        min_question_length: int = 15,
        min_answer_length: int = 50,
        min_stackoverflow_score: int = 5,
    ):

        self.min_question_length = (
            min_question_length
        )

        self.min_answer_length = (
            min_answer_length
        )

        self.min_stackoverflow_score = (
            min_stackoverflow_score
        )

    def remove_html(
        self,
        text: str,
    ) -> str:
        """
        Remove HTML tags and entities.
        """

        if not text:
            return ""

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

    def remove_short_answers(
        self,
        records,
    ):
        """
        Remove records having very short answers.
        """

        filtered = []

        for record in records:

            answer = record.get(
                "answer",
                "",
            )

            if (
                len(answer.strip())
                >= self.min_answer_length
            ):
                filtered.append(record)

        return filtered

    def remove_low_score_so_questions(
        self,
        records,
    ):
        """
        Remove only low-quality StackOverflow records.

        Other sources are not affected.
        """

        filtered = []

        for record in records:

            source = (
                record.get(
                    "source",
                    "",
                )
                .strip()
                .lower()
            )

            if source == "stackoverflow":

                score = int(
                    record.get(
                        "score",
                        0,
                    )
                )

                if (
                    score
                    < self.min_stackoverflow_score
                ):
                    continue

            filtered.append(record)

        return filtered

    def technical_term_density(
        self,
        text: str,
    ) -> int:
        """
        Count technical keywords.
        """

        words = text.lower().split()

        count = 0

        for word in words:

            word = word.strip(
                ".,!?()[]{}:;\"'"
            )

            if word in self.TECH_KEYWORDS:
                count += 1

        return count

    def assign_quality_score(
        self,
        record,
    ) -> float:
        """
        Assign dataset quality score (0-100).
        """

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

        source = (
            record.get(
                "source",
                "",
            )
            .strip()
            .lower()
        )

        score = 0

        #
        # Question Length (20)
        #

        score += (
            min(
                len(question) / 80,
                1,
            )
            * 20
        )

        #
        # Answer Length (30)
        #

        score += (
            min(
                len(answer) / 500,
                1,
            )
            * 30
        )

        #
        # Source Quality
        #

        if source == "stackoverflow":

            score += (
                min(
                    so_score / 100,
                    1,
                )
                * 25
            )

            if accepted:
                score += 15

        else:

            #
            # Other sources receive
            # full source-quality score.
            #

            score += 40

        #
        # Technical keyword density (10)
        #

        technical_terms = (
            self.technical_term_density(
                question + " " + answer
            )
        )

        score += (
            min(
                technical_terms / 10,
                1,
            )
            * 10
        )

        return round(
            min(score, 100),
            2,
        )

    def filter_records(
    self,
    records,
    minimum_quality: float = 40,
    ):
        """
        Clean and filter dataset.
        """

        cleaned_records = []

        for record in records:

            record["question"] = (
                self.remove_html(
                    record.get(
                        "question",
                        "",
                    )
                )
            )

            record["answer"] = (
                self.remove_html(
                    record.get(
                        "answer",
                        "",
                    )
                )
            )

            #
            # Question length validation
            #

            if (
                len(record["question"])
                < self.min_question_length
            ):
                continue

            quality = (
                self.assign_quality_score(
                    record
                )
            )

            record[
                "quality_score"
            ] = quality

            if (
                quality
                >= minimum_quality
            ):
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

    sample_record = {
        "question":
            "<b>What is Python?</b>",

        "answer":
            "<p>Python is a high-level interpreted programming language used in web development, automation, artificial intelligence, data science, scripting, APIs, machine learning, and software engineering.</p>",

        "score":
            120,

        "accepted_answer":
            "12345",

        "source":
            "StackOverflow",
    }

    sample_record["question"] = (
        engine.remove_html(
            sample_record["question"]
        )
    )

    sample_record["answer"] = (
        engine.remove_html(
            sample_record["answer"]
        )
    )

    sample_record[
        "quality_score"
    ] = (
        engine.assign_quality_score(
            sample_record
        )
    )

    print("\nProcessed Record:\n")

    print(sample_record)