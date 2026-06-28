"""
GeeksforGeeks Interview Question Scraper

Purpose:
Collect high-quality interview Q&A pairs
from multiple GeeksforGeeks sources.

Output:
datasets/raw/gfg_python_qa.csv
"""

import csv
import time
import requests

from pathlib import Path
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    PROJECT_ROOT /
    "datasets" /
    "raw" /
    "gfg_python_qa.csv"
)


URLS = [

    # Python

    "https://www.geeksforgeeks.org/python-interview-questions/",
    "https://www.geeksforgeeks.org/python-oops-interview-questions/",
    "https://www.geeksforgeeks.org/advanced-python-interview-questions/",

    # SQL

    "https://www.geeksforgeeks.org/sql-interview-questions/",
    "https://www.geeksforgeeks.org/pl-sql-interview-questions/",

    # Machine Learning

    "https://www.geeksforgeeks.org/machine-learning-interview-questions/",
    "https://www.geeksforgeeks.org/deep-learning-interview-questions/",
    "https://www.geeksforgeeks.org/nlp-interview-questions/",

    # Data Engineering

    "https://www.geeksforgeeks.org/data-engineer-interview-questions/",
    "https://www.geeksforgeeks.org/etl-testing-interview-questions/",

    # Big Data

    "https://www.geeksforgeeks.org/apache-spark-interview-questions/",
    "https://www.geeksforgeeks.org/hadoop-interview-questions/",
    "https://www.geeksforgeeks.org/apache-kafka-interview-questions/",

    # Backend / APIs

    "https://www.geeksforgeeks.org/django-interview-questions/",
    "https://www.geeksforgeeks.org/flask-interview-questions/",
    "https://www.geeksforgeeks.org/rest-api-interview-questions/",

    # General CS

    "https://www.geeksforgeeks.org/oops-interview-questions/",
    "https://www.geeksforgeeks.org/dbms-interview-questions/",
    "https://www.geeksforgeeks.org/os-interview-questions/",
    "https://www.geeksforgeeks.org/computer-network-interview-questions/",
]


class GFGScraper:
    """
    GeeksforGeeks scraper.
    """

    def __init__(self):

        self.headers = {
            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
        }

        self.seen_questions = set()

    def fetch_page(
        self,
        url,
        max_retries=3
    ):
        """
        Fetch page with retry logic.
        """

        for attempt in range(max_retries):

            try:

                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=20
                )

                response.raise_for_status()

                return response.text

            except Exception as error:

                print(
                    f"Attempt {attempt + 1} failed "
                    f"for {url}"
                )

                print(error)

                time.sleep(2)

        print(
            f"Failed to download: {url}"
        )

        return ""

    def is_valid_question(
        self,
        question
    ):
        """
        Validate extracted question.
        """

        question = question.strip()

        if len(question) < 10:
            return False

        if len(question) > 250:
            return False

        if "?" not in question:
            return False

        invalid_terms = [

            "table of contents",
            "read more",
            "download pdf",
            "navigation",
            "next article",
            "previous article",
            "must read",
            "related articles",
            "share this article",
        ]

        lower_question = (
            question.lower()
        )

        for term in invalid_terms:

            if term in lower_question:
                return False

        return True

    def infer_topic(
        self,
        url
    ):
        """
        Infer topic from URL.
        """

        url = url.lower()

        if "python" in url:
            return "Python"

        if "sql" in url:
            return "SQL"

        if "spark" in url:
            return "Spark"

        if "kafka" in url:
            return "Kafka"

        if "machine-learning" in url:
            return "Machine Learning"

        if "deep-learning" in url:
            return "Deep Learning"

        if "nlp" in url:
            return "NLP"

        if "django" in url:
            return "Django"

        if "flask" in url:
            return "Flask"

        return "General"

    def extract_questions_answers(
        self,
        html,
        source_url
    ):
        """
        Extract Q&A pairs.
        """

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        records = []

        headings = soup.find_all(
            ["h2", "h3"]
        )

        for heading in headings:

            question = (
                heading.get_text(
                    strip=True
                )
            )

            if not self.is_valid_question(
                question
            ):
                continue

            normalized = (
                question.lower()
            )

            if normalized in self.seen_questions:
                continue

            self.seen_questions.add(
                normalized
            )

            answer_parts = []

            sibling = (
                heading.find_next_sibling()
            )

            while sibling:

                if sibling.name in [
                    "h2",
                    "h3"
                ]:
                    break

                text = sibling.get_text(
                    " ",
                    strip=True
                )

                if text:

                    answer_parts.append(
                        text
                    )

                sibling = (
                    sibling.find_next_sibling()
                )

            answer = " ".join(
                answer_parts
            )

            if len(answer) < 30:
                continue

            records.append(
                {
                    "question":
                        question,

                    "answer":
                        answer,

                    "topic":
                        self.infer_topic(
                            source_url
                        ),

                    "source":
                        "GeeksforGeeks",

                    "url":
                        source_url,

                    "difficulty":
                        "Medium"
                }
            )

        return records

    def save_dataset(
        self,
        records
    ):
        """
        Save records to CSV.
        """

        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "question",
                    "answer",
                    "topic",
                    "source",
                    "url",
                    "difficulty"
                ]
            )

            writer.writeheader()

            writer.writerows(
                records
            )

        print(
            f"\nSaved {len(records)} records"
        )

        print(
            f"\nDataset Path:\n"
            f"{OUTPUT_FILE}"
        )


def main():

    scraper = GFGScraper()

    all_records = []

    for url in URLS:

        print(
            f"\nScraping:\n{url}"
        )

        html = scraper.fetch_page(
            url
        )

        if not html:
            continue

        records = (
            scraper.extract_questions_answers(
                html,
                url
            )
        )

        print(
            f"Collected "
            f"{len(records)} records"
        )

        all_records.extend(
            records
        )

    scraper.save_dataset(
        all_records
    )

    print(
        f"\nTotal Unique Records: "
        f"{len(all_records)}"
    )


if __name__ == "__main__":
    main()