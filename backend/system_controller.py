"""
System Controller

Purpose:
Central orchestration layer.

Frontend
    ↓
SystemController
    ↓
Backend Modules
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.resume_parser import (
    ResumeParser,
)

from ml_models.role_prediction.train_role_classifier import (
    RoleClassifier,
)

from backend.interview_session import (
    InterviewSession,
)


class SystemController:

    def __init__(self):

        self.resume_parser = (
            ResumeParser()
        )

        self.role_classifier = (
            RoleClassifier()
        )

        self.interview_session = (
            InterviewSession()
        )

    # --------------------------------------------------
    # Complete Resume Pipeline
    # --------------------------------------------------

    def run_complete_pipeline(
        self,
        resume_path
    ):
        """
        Execute:

        Resume
            ↓
        Parsing
            ↓
        Skill Extraction
            ↓
        Role Prediction
        """

        parsed_data = (
            self.resume_parser.parse_resume(
                resume_path
            )
        )

        try:

            self.role_classifier.load_model()

            role = (
                self.role_classifier.predict_role(
                    parsed_data["cleaned_text"]
                )
            )

        except Exception:

            role = (
                "Python Developer"
            )

        return {
            "skills":
                parsed_data["skills"],

            "cleaned_text":
                parsed_data["cleaned_text"],

            "role":
                role
        }

    # --------------------------------------------------
    # Interview Session
    # --------------------------------------------------

    def start_interview(
        self,
        role
    ):

        self.interview_session.start_session(
            role
        )

    def ask_question(self):

        return (
            self.interview_session.ask_question()
        )

    def submit_answer(
        self,
        answer
    ):

        self.interview_session.submit_answer(
            answer
        )

    def evaluate_answer(self):

        return (
            self.interview_session.evaluate_answer()
        )

    def generate_report(self):

        return (
            self.interview_session.generate_report()
        )


def main():

    controller = (
        SystemController()
    )

    print(
        "System Controller initialized."
    )


if __name__ == "__main__":
    main()