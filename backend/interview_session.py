"""
Interview Session Orchestrator

Purpose:
Manage the interview workflow by coordinating:

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
from typing import Dict, List

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
        self.expected_answer = None
        self.current_answer = None

        self.session_history: List[Dict] = []

        self.session_completed = False

    def start_session(
        self,
        predicted_role: str,
    ) -> None:
        """
        Start interview session.
        """

        self.current_role = predicted_role

        print("\nInterview Session Started")
        print(f"Role: {predicted_role}")

    def ask_question(self) -> str:
        """
        Generate an interview question using the
        QuestionGenerationAgent.
        """

        if self.current_role is None:
            raise RuntimeError(
                "Interview session has not been started."
            )

        result = (
            self.question_agent.generate_question(
                self.current_role
            )
        )

        if not isinstance(result, dict):
            raise TypeError(
                "QuestionGenerationAgent must return "
                "a dictionary containing "
                "'question' and 'expected_answer'."
            )

        if (
            "question" not in result
            or "expected_answer" not in result
        ):
            raise KeyError(
                "Missing required keys: "
                "'question' or 'expected_answer'."
            )

        self.current_question = result["question"]

        self.expected_answer = (
            result["expected_answer"]
        )

        return self.current_question

    def submit_answer(
        self,
        answer: str,
    ) -> None:
        """
        Store candidate answer for the
        current interview question.
        """

        if self.current_question is None:
            raise RuntimeError(
                "No active question. "
                "Generate a question before "
                "submitting an answer."
            )

        if not answer.strip():
            raise ValueError(
                "Candidate answer cannot be empty."
            )

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

        # Reset current question state
        self.current_question = None
        self.expected_answer = None
        self.current_answer = None

        return result

    def generate_report(self) -> Dict:
        """
        Generate interview summary.
        """

        total_questions = len(
            self.session_history
        )

        if total_questions == 0:

            return {
                "role": self.current_role,
                "total_questions": 0,
                "average_score": 0,
                "overall_result": (
                    "No Interview Conducted"
                ),
                "details": [],
            }

        total_score = sum(
            record["score"]
            for record in self.session_history
        )

        average_score = round(
            total_score / total_questions,
            2,
        )

        report = {
            "role": self.current_role,
            "total_questions": total_questions,
            "average_score": average_score,
            "overall_result": overall_result,
            "details": self.session_history,
        }

        return report


def main():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    question = session.ask_question()

    print("\nQuestion:")
    print(question)

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
