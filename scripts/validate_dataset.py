"""
Dataset Validation Script

Purpose:
Validate scraped interview question datasets before cleaning
and chunking.

Metrics:

* Total Questions
* Unique Questions
* Duplicate Questions
* Duplicate Percentage
* Empty Lines
* Short Questions
* Long Questions
* Average Length
  """

from pathlib import Path

DATASET_PATH = Path(
"datasets/raw/python_questions.txt"
)

def main():
    with open(
    DATASET_PATH,
    "r",
    encoding="utf-8"
    ) as file:
        questions = file.readlines()


    questions = [
        question.strip()
        for question in questions
    ]

    total_questions = len(questions)

    unique_questions = len(
        set(questions)
    )

    duplicates = (
        total_questions -
        unique_questions
    )

    duplicate_percentage = 0

    if total_questions > 0:
        duplicate_percentage = (
            duplicates /
            total_questions
        ) * 100

    empty_lines = sum(
        1
        for question in questions
        if not question
    )

    short_questions = sum(
        1
        for question in questions
        if len(question) < 10
    )

    long_questions = sum(
        1
        for question in questions
        if len(question) > 300
    )

    non_empty_questions = [
        question
        for question in questions
        if question
    ]

    average_length = 0

    if non_empty_questions:
        average_length = (
            sum(
                len(question)
                for question in non_empty_questions
            )
            /
            len(non_empty_questions)
        )

    print(
        f"Total Questions: {total_questions}"
    )

    print(
        f"Unique Questions: {unique_questions}"
    )

    print(
        f"Duplicates: {duplicates}"
    )

    print(
        f"Duplicate %: "
        f"{duplicate_percentage:.2f}%"
    )

    print(
        f"Empty Lines: {empty_lines}"
    )

    print(
        f"Short Questions: "
        f"{short_questions}"
    )

    print(
        f"Long Questions: "
        f"{long_questions}"
    )

    print(
        f"Average Length: "
        f"{average_length:.2f}"
    )


if __name__ == "__main__":
    main()
