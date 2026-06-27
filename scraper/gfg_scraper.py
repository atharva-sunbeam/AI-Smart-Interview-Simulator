"""
GeeksforGeeks Interview Question Scraper

Purpose:
Scrape interview questions and answers
from GeeksforGeeks pages.

Output:
datasets/raw/gfg_python_qa.csv
"""

import csv
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


class GFGScraper:
    """
    Scraper for GeeksforGeeks
    interview question pages.
    """

    def __init__(self):

        self.headers = {
            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
        }

    def fetch_page(
        self,
        url
    ):
        """
        Download webpage HTML.
        """

        response = requests.get(
            url,
            headers=self.headers,
            timeout=20
        )

        response.raise_for_status()

        return response.text

    def extract_questions_answers(
        self,
        html,
        source_url
    ):
        """
        Extract questions and answers.

        GFG commonly stores questions
        inside h2/h3 tags.
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

            question = heading.get_text(
                strip=True
            )

            if "?" not in question:
                continue

            answer_parts = []

            sibling = heading.find_next_sibling()

            while sibling:

                if sibling.name in ["h2", "h3"]:
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

            if not answer:
                continue

            records.append(
                {
                    "question": question,
                    "answer": answer,
                    "topic": "Python",
                    "source": "GeeksforGeeks",
                    "url": source_url,
                    "difficulty": "Medium"
                }
            )

        return records

    def save_dataset(
        self,
        records
    ):
        """
        Save extracted records.
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

            writer.writerows(records)

        print(
            f"\nSaved {len(records)} records"
        )

        print(
            f"Dataset Path:\n{OUTPUT_FILE}"
        )


def main():

    scraper = GFGScraper()

    urls = [
        (
            "https://www.geeksforgeeks.org/"
            "python-interview-questions/"
        )
    ]

    all_records = []

    for url in urls:

        print(
            f"\nScraping:\n{url}"
        )

        html = scraper.fetch_page(
            url
        )

        records = (
            scraper.extract_questions_answers(
                html,
                url
            )
        )

        all_records.extend(records)

    scraper.save_dataset(
        all_records
    )


if __name__ == "__main__":
    main()