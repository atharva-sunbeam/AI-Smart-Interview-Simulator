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
"""
Interview Session Orchestrator

Purpose:
Manage interview flow by coordinating:

Role
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

from agents.answer_evaluation_agent import (
    AnswerEvaluationAgent,
)


class InterviewSession:
    """
    Orchestrates an interview session.
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

        self.session_completed = False

    def start_session(
        self,
        predicted_role: str,
    ) -> None:
        """
        Initialize interview session.
        """

        self.current_role = predicted_role

        print("\nInterview Session Started")

        print(
            f"Role: {predicted_role}"
        )

    def ask_question(
        self,
    ) -> str:
        """
        Generate interview question.
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

        self.current_question = (
            result["question"]
        )

        self.expected_answer = (
            result["expected_answer"]
        )

        return self.current_question

    def submit_answer(
        self,
        answer: str,
    ) -> None:
        """
        Store candidate answer.
        """

        if not answer.strip():
            raise ValueError(
                "Candidate answer cannot be empty."
            )

        self.current_answer = answer

        print(
            "\nAnswer submitted successfully."
        )

    def evaluate_answer(
        self,
    ) -> dict:
        """
        Evaluate current answer using
        AnswerEvaluationAgent.
        """

        if self.expected_answer is None:
            raise RuntimeError(
                "No question available for evaluation."
            )

        if self.current_answer is None:
            raise RuntimeError(
                "No candidate answer submitted."
            )

        result = (
            self.evaluator.evaluate_answer(
                expected_answer=self.expected_answer,
                candidate_answer=self.current_answer,
            )
        )

        interview_record = {
            "role": self.current_role,
            "question": self.current_question,
            "expected_answer": self.expected_answer,
            "candidate_answer": self.current_answer,
            "score": result["score"],
            "similarity": result["similarity"],
            "feedback": result["feedback"],
        }

        self.session_history.append(
            interview_record
        )

        # Clear current state
        self.current_question = None
        self.current_answer = None
        self.expected_answer = None

        return result

    def generate_report(
        self,
    ) -> dict:
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
                "overall_result": "No Interview Conducted",
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

        if average_score >= 80:
            overall_result = "Excellent"

        elif average_score >= 60:
            overall_result = "Good"

        else:
            overall_result = (
                "Needs Improvement"
            )

        self.session_completed = True

        return {
            "role": self.current_role,
            "total_questions": total_questions,
            "average_score": average_score,
            "overall_result": overall_result,
            "details": self.session_history,
        }


if __name__ == "__main__":

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    question = session.ask_question()

    print("\nQuestion:")
    print(question)

    session.submit_answer(
        "Decorators modify the behaviour of functions."
    )

    result = session.evaluate_answer()

    print("\nEvaluation Result")
    print(result)

    report = session.generate_report()

    print("\nInterview Report")
    print(report)

class InterviewSession:

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

        result = (
            self.evaluator.evaluate_answer(
                expected_answer=self.expected_answer,
                candidate_answer=self.current_answer
            )
        )

        interview_record = {
            "role": self.current_role,
            "question": self.current_question,
            "expected_answer": self.expected_answer,
            "candidate_answer": self.current_answer,
            "score": result["score"],
            "feedback": result["feedback"],
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

        return {
            "role": self.current_role,
            "total_questions": total_questions,
            "average_score": round(
                average_score,
                2
            ),
            "details": self.session_history,
        }


if __name__ == "__main__":

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
        "Decorators modify the behavior of functions."
    )

    print(
        session.evaluate_answer()
    )

    print(
        session.generate_report()
    )