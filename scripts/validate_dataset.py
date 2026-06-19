from collections import Counter

DATASET_PATH = "datasets/raw/python_questions.txt"


def main():
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as file:
            lines = file.readlines()

        total_lines = len(lines)

        empty_lines = sum(1 for line in lines if not line.strip())

        questions = [line.strip() for line in lines if line.strip()]

        total_questions = len(questions)

        unique_questions = len(set(questions))

        duplicates = total_questions - unique_questions

        average_length = (
            sum(len(question) for question in questions) / total_questions
            if total_questions > 0
            else 0
        )

        print(f"Total Questions: {total_questions}")
        print(f"Unique Questions: {unique_questions}")
        print(f"Duplicates: {duplicates}")
        print(f"Empty Lines: {empty_lines}")
        print(f"Average Length: {average_length:.2f} characters")

    except FileNotFoundError:
        print(f"Dataset not found: {DATASET_PATH}")


if __name__ == "__main__":
    main()