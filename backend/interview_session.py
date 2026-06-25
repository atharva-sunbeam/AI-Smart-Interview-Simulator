"""
Interview Session Orchestrator

Purpose:
Coordinate the complete interview workflow.

Pipeline:

Resume
    ↓
Role Prediction
    ↓
Question Generation
    ↓
Candidate Answer
    ↓
Answer Evaluation
    ↓
Interview Report
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.question_generation_agent import (
    QuestionGenerationAgent,
)


class InterviewSession:
    """
    Orchestrates the complete interview process.
    """

    def __init__(self):

        self.question_agent = (
            QuestionGenerationAgent()
        )

        self.current_role = None
        self.current_question = None
        self.current_answer = None

        self.session_history = []

    def start_session(
        self,
        predicted_role
    ):
        """
        Start interview session.
        """

        self.current_role = predicted_role

        print(
            f"\nInterview Session Started"
        )

        print(
            f"Role: {predicted_role}"
        )

    def ask_question(self):
        """
        Generate and return interview question.
        """

        self.current_question = (
            self.question_agent.generate_question(
                self.current_role
            )
        )

        return self.current_question

    def submit_answer(
        self,
        answer
    ):
        """
        Store candidate answer.
        """

        self.current_answer = answer

        print(
            "\nAnswer submitted successfully."
        )

    def evaluate_answer(self):
        """
        Placeholder evaluation.

        Will later integrate:
        AnswerEvaluationAgent
        """

        score = 8

        feedback = (
            "Good answer. Demonstrates "
            "basic understanding."
        )

        interview_record = {
            "role": self.current_role,
            "question": self.current_question,
            "answer": self.current_answer,
            "score": score,
            "feedback": feedback,
        }

        self.session_history.append(
            interview_record
        )

        return {
            "score": score,
            "feedback": feedback,
        }

    def generate_report(self):
        """
        Generate final interview report.
        """

        total_questions = len(
            self.session_history
        )

        if total_questions == 0:

            return {
                "total_questions": 0,
                "average_score": 0,
            }

        total_score = sum(
            record["score"]
            for record in self.session_history
        )

        average_score = (
            total_score / total_questions
        )

        report = {
            "role": self.current_role,
            "total_questions": total_questions,
            "average_score": round(
                average_score,
                2,
            ),
            "details": self.session_history,
        }

        return report


def main():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    question = session.ask_question()

    print(
        f"\nQuestion:\n{question}"
    )

    candidate_answer = (
        "Decorators modify the "
        "behavior of functions."
    )

    session.submit_answer(
        candidate_answer
    )

    evaluation = (
        session.evaluate_answer()
    )

    print(
        "\nEvaluation:"
    )

    print(evaluation)

    report = (
        session.generate_report()
    )

    print(
        "\nFinal Report:\n"
    )

    print(report)


if __name__ == "__main__":
    main()