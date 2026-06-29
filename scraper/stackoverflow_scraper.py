"""
Stack Overflow Scraper

Purpose:
Collect high-quality technical Question-Answer pairs
using the official Stack Exchange API.

Topics:
- Python
- SQL
- Machine Learning
- Apache Kafka
- Apache Spark

Output:
datasets/raw/stackoverflow_qa.csv
"""

import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class StackOverflowScraper:
    """
    Collect technical Q&A pairs from Stack Overflow.
    """

    QUESTIONS_API_URL = (
        "https://api.stackexchange.com/2.3/questions"
    )

    ANSWERS_API_URL = (
        "https://api.stackexchange.com/2.3/answers"
    )

    TAGS = [
        "python",
        "sql",
        "machine-learning",
        "apache-kafka",
        "apache-spark",
    ]

    def __init__(self):
        """
        Initialize scraper.
        """
        self.answer_cache = {}

    def fetch_questions(
        self,
        tag: str,
        page: int = 1,
        pagesize: int = 100,
    ):
        """
        Fetch questions for a given tag.
        """

        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": tag,
            "site": "stackoverflow",
            "filter": "default",
            "page": page,
            "pagesize": pagesize,
        }

        response = requests.get(
            self.QUESTIONS_API_URL,
            params=params,
            timeout=30,
        )

        if response.status_code != 200:

            print(
                f"\nFailed to fetch "
                f"questions for tag '{tag}'"
            )

            print(
                f"Status Code: "
                f"{response.status_code}"
            )

            print(response.text)

            return None

        return response.json()

    def fetch_answer(
        self,
        answer_id: int,
    ):
        """
        Retrieve accepted answer body.
        """

        if answer_id in self.answer_cache:
            return self.answer_cache[answer_id]

        url = (
            f"{self.ANSWERS_API_URL}/{answer_id}"
        )

        params = {
            "site": "stackoverflow",
            "filter": "withbody",
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30,
            )

            if response.status_code != 200:

                print(
                    f"\nFailed to fetch answer "
                    f"{answer_id}"
                )

                print(
                    f"Status Code: "
                    f"{response.status_code}"
                )

                print(response.text)

                return ""

            data = response.json()

            items = data.get(
                "items",
                [],
            )

            if not items:

                self.answer_cache[
                    answer_id
                ] = ""

                return ""

            html = items[0].get(
                "body",
                "",
            )

            cleaned_answer = BeautifulSoup(
                html,
                "html.parser",
            ).get_text(
                separator=" ",
                strip=True,
            )

            self.answer_cache[
                answer_id
            ] = cleaned_answer

            return cleaned_answer

        except requests.exceptions.RequestException as e:

            print(
                f"Skipping answer {answer_id}: {e}"
            )

            self.answer_cache[answer_id] = ""
            return ""

    def parse_questions(
    self,
    api_response,
    ):
        """
        Extract high-quality records.
        """

        records = []

        for item in api_response.get(
            "items",
            [],
        ):

            if item.get(
                "score",
                0,
            ) < 5:
                continue

            if not item.get(
                "accepted_answer_id"
            ):
                continue

            #
            # Unit tests may directly provide
            # accepted_answer.
            #

            answer = item.get(
                "accepted_answer",
                ""
            )

            #
            # Production mode:
            # fetch answer from API.
            #

            if not answer:

                answer = self.fetch_answer(
                    item[
                        "accepted_answer_id"
                    ]
                )

            if not answer:
                continue

            records.append(
                {
                    "question": item.get(
                        "title",
                        "",
                    ),

                    "answer": answer,

                    "body": item.get(
                        "body",
                        "",
                    ),

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

                    "accepted_answer": (
                        answer
                    ),

                    "accepted_answer_id": (
                        item.get(
                            "accepted_answer_id"
                        )
                    ),

                    "url": item.get(
                        "link",
                        "",
                    ),

                    "source":
                        "StackOverflow",
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
        Save dataset to CSV.
        """

        output_path = Path(
            output_file
        )

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

            writer.writerows(
                records
            )

    def collect_dataset(
        self,
        pages_per_tag: int = 2,
    ):
        """
        Collect Q&A pairs for all tags.
        """

        all_records = []

        for tag in self.TAGS:

            print(
                f"\nCollecting tag: {tag}"
            )

            for page in range(
                1,
                pages_per_tag + 1,
            ):

                print(
                    f"Page {page}"
                )

                response = self.fetch_questions(
                    tag=tag,
                    page=page,
                )

                # Skip failed requests
                if response is None:
                    print(
                        f"Skipping {tag} page {page}"
                    )
                    continue

                records = self.parse_questions(
                    response
                )
                print(
                    f"Collected {len(records)} records."
                )

                all_records.extend(
                    records
                )

        self.save_dataset(
            all_records
        )

        print(
            f"\nDataset saved successfully."
        )

        print(
            f"Total records: "
            f"{len(all_records)}"
        )


def main():

    scraper = (
        StackOverflowScraper()
    )

    scraper.collect_dataset(
        pages_per_tag=2
    )


if __name__ == "__main__":
    main()
