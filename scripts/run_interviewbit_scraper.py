import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from scraper.interviewbit_scraper import (
InterviewBitScraper
)

def main():
    scraper = InterviewBitScraper()


    questions = scraper.fetch_questions()

    output_dir = Path(
        "datasets/raw"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        "python_questions.txt"
    )

    data = "\n".join(questions)

    scraper.save_to_file(
        output_file,
        data
    )

    print(
        f"Saved {len(questions)} "
        f"questions to {output_file}"
    )

    if __name__ == "__main__":
        main()
