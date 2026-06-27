"""
Interview Session Orchestrator
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.question_generation_agent import (
    QuestionGenerationAgent,
)

from agents.answer_evaluation_agent import (
    AnswerEvaluationAgent,
)


class InterviewSession:
    """
    Orchestrates the complete interview process.
    """

    def __init__(self):

        self.question_agent = (
            QuestionGenerationAgent()
        )

        self.evaluator = (
            AnswerEvaluationAgent()
        )

        self.current_role = None
        self.current_question = None
        self.current_answer = None
        self.expected_answer = None

        self.session_history = []

    def start_session(
        self,
        predicted_role
    ):

        self.current_role = predicted_role

        print(
            "\nInterview Session Started"
        )

        print(
            f"Role: {predicted_role}"
        )

    def ask_question(self):

        result = (
            self.question_agent.generate_question(
                self.current_role
            )
        )

        self.current_question = (
            result["question"]
        )

        self.expected_answer = (
            result["expected_answer"]
        )

        return self.current_question

    def submit_answer(
        self,
        answer
    ):

        self.current_answer = answer

        print(
            "\nAnswer submitted successfully."
        )

    def evaluate_answer(self):
        """
        Evaluate candidate answer.
        """

        if not self.expected_answer:

            self.expected_answer = (
                "Reference answer not available."
            )

        if not self.current_answer:

            self.current_answer = ""

        result = (
            self.evaluator.evaluate_answer(
                expected_answer=
                    self.expected_answer,

                candidate_answer=
                    self.current_answer
            )
        )

        interview_record = {

            "role":
                self.current_role,

            "question":
                self.current_question,

            "expected_answer":
                self.expected_answer,

            "candidate_answer":
                self.current_answer,

            "score":
                result["score"],

            "feedback":
                result["feedback"],
        }

        self.session_history.append(
            interview_record
        )

        return result

    def generate_report(self):

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
                2
            ),
            "details": self.session_history,
        }

        return report


def main():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    question = (
        session.ask_question()
    )

    print(
        f"\nQuestion:\n{question}"
    )

    session.submit_answer(
        "Decorators modify functions."
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