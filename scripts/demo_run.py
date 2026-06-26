"""
Demo Runner

Purpose:
Demonstrate the complete interview workflow
without Streamlit.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.interview_session import InterviewSession


def main():

    print("=" * 60)
    print("AI Smart Interview Simulator Demo")
    print("=" * 60)

    session = InterviewSession()

    role = "Data Engineer"

    session.start_session(role)

    question = session.ask_question()

    print(f"\nPredicted Role: {role}")

    print("\nQuestion:")
    print(question)

    candidate_answer = (
        "Kafka partitions improve scalability "
        "by distributing messages across brokers."
    )

    print("\nCandidate Answer:")
    print(candidate_answer)

    session.submit_answer(candidate_answer)

    result = session.evaluate_answer()

    print("\nEvaluation")

    print(f"Score      : {result['score']}")

    print(f"Similarity : {result['similarity']}")

    print(f"Feedback   : {result['feedback']}")

    report = session.generate_report()

    print("\nInterview Report")

    print(report)

    print("\nDemo completed successfully.")


if __name__ == "__main__":
    main()