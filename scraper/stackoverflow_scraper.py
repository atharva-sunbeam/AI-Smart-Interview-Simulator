"""
Stack Overflow Scraper

Purpose:
Collect technical Question-Answer pairs
using the Stack Exchange API.

Topics:
- Python
- SQL
- Machine Learning
- Kafka
- Spark
"""

import csv
from pathlib import Path

import requests


class StackOverflowScraper:

    API_URL = (
        "https://api.stackexchange.com/2.3/questions"
    )

    TAGS = [
        "python",
        "sql",
        "machine-learning",
        "apache-kafka",
        "apache-spark",
    ]

    def fetch_questions(
        self,
        tag: str,
        page: int = 1,
        pagesize: int = 100,
    ):
        """
        Fetch questions from Stack Exchange API.
        """

        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": tag,
            "site": "stackoverflow",
            "filter": "withbody",
            "page": page,
            "pagesize": pagesize,
        }

        response = requests.get(
            self.API_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def parse_questions(
        self,
        api_response,
    ):
        """
        Extract required fields.
        """

        records = []

        for item in api_response.get(
            "items",
            [],
        ):

            records.append(
                {
                    "question": item.get(
                        "title",
                        "",
                    ),
                    "answer": "",
                    "tags": ",".join(
                        item.get(
                            "tags",
                            [],
                        )
                    ),
                    "score": item.get(
                        "score",
                        0,
                    ),
                    "accepted_answer": item.get(
                        "accepted_answer_id",
                        "",
                    ),
                    "url": item.get(
                        "link",
                        "",
                    ),
                }
            )

        return records

    def save_dataset(
        self,
        records,
        output_file=(
            "datasets/raw/"
            "stackoverflow_qa.csv"
        ),
    ):
        """
        Save dataset.
        """

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "question",
                    "answer",
                    "tags",
                    "score",
                    "accepted_answer",
                    "url",
                ],
            )

            writer.writeheader()
            writer.writerows(records)

    def collect_dataset(
        self,
        pages_per_tag=2,
    ):
        """
        Collect data for all tags.
        """

        all_records = []

        for tag in self.TAGS:

            for page in range(
                1,
                pages_per_tag + 1,
            ):

                print(
                    f"Fetching {tag} "
                    f"(page {page})"
                )

                data = self.fetch_questions(
                    tag=tag,
                    page=page,
                )

                all_records.extend(
                    self.parse_questions(
                        data
                    )
                )

        self.save_dataset(
            all_records
        )

        print(
            f"Saved {len(all_records)} "
            "records."
        )


if __name__ == "__main__":

    scraper = StackOverflowScraper()

    scraper.collect_dataset()