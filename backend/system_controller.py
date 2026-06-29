"""
System Controller

Purpose:
Central orchestration layer.
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
    """
    Central orchestration layer.
    """

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

    def run_complete_pipeline(
        self,
        resume_path
    ):
        """
        Complete resume processing pipeline.

        Resume
            ↓
        Resume Parsing
            ↓
        Role Prediction
        """

        try:

            if not Path(
                resume_path
            ).exists():

                raise FileNotFoundError

            parsed_data = (
                self.resume_parser.parse_resume(
                    resume_path
                )
            )

        except FileNotFoundError:

            print(
                "Resume file not found."
            )

            return {

                "skills": [],

                "cleaned_text": "",

                "role":
                    "Python Developer",
            }

        except Exception as error:

            print(
                f"Resume parsing failed: "
                f"{error}"
            )

            return {

                "skills": [],

                "cleaned_text": "",

                "role":
                    "Python Developer",
            }

        if not parsed_data.get(
            "cleaned_text"
        ):

            print(
                "Empty resume text."
            )

            return {

                "skills":
                    parsed_data.get(
                        "skills",
                        []
                    ),

                "cleaned_text": "",

                "role":
                    "Python Developer",
            }

        try:

            self.role_classifier.load_model()

            role = (
                self.role_classifier.predict_role(
                    parsed_data[
                        "cleaned_text"
                    ]
                )
            )

        except FileNotFoundError:

            print(
                "Role model not found."
            )

            role = (
                "Python Developer"
            )

        except Exception as error:

            print(
                f"Prediction error: "
                f"{error}"
            )

            role = (
                "Python Developer"
            )

        return {

            "skills":
                parsed_data.get(
                    "skills",
                    []
                ),

            "cleaned_text":
                parsed_data.get(
                    "cleaned_text",
                    ""
                ),

            "role":
                role
        }

    def start_interview(
        self,
        role
    ):
        """
        Start interview session.
        """

        self.interview_session.start_session(
            role
        )

    def ask_question(
        self
    ):
        """
        Generate interview question.
        """

        try:

            return (
                self.interview_session.ask_question()
            )

        except FileNotFoundError:

            print(
                "Embeddings file missing."
            )

            return {

                "question":
                    "Explain Python decorators.",

                "expected_answer":
                    "Decorators extend the behaviour "
                    "of functions without modifying "
                    "their source code.",

                "audio_path":
                    None,

                "question_number":
                    (
                        self.interview_session
                        .questions_asked + 1
                    ),

                "max_questions":
                    (
                        self.interview_session
                        .max_questions
                    ),

                "difficulty":
                    (
                        self.interview_session
                        .current_difficulty
                    ),
            }

        except Exception as error:

            print(
                f"Retriever error: "
                f"{error}"
            )

            return {

                "question":
                    "Explain Python decorators.",

                "expected_answer":
                    "Decorators extend the behaviour "
                    "of functions without modifying "
                    "their source code.",

                "audio_path":
                    None,

                "question_number":
                    (
                        self.interview_session
                        .questions_asked + 1
                    ),

                "max_questions":
                    (
                        self.interview_session
                        .max_questions
                    ),

                "difficulty":
                    (
                        self.interview_session
                        .current_difficulty
                    ),
            }

    def submit_answer(
        self,
        answer
    ):
        """
        Submit candidate answer.
        """

        if not answer.strip():

            raise ValueError(
                "Candidate answer is empty."
            )

        self.interview_session.submit_answer(
            answer
        )

    def evaluate_answer(
        self,
    ):
        """
        Evaluate candidate answer.
        """

        try:

            return (
                self.interview_session.evaluate_answer()
            )

        except Exception as error:

            print(
                f"Evaluation failed: "
                f"{error}"
            )

            return {

                "score": 0,

                "similarity": 0,

                "feedback":
                    "Evaluation unavailable."
            }

    def generate_report(
        self,
    ):
        """
        Generate interview report.
        """

        return (
            self.interview_session.generate_report()
        )


if __name__ == "__main__":

    controller = (
        SystemController()
    )

    print(
        "System Controller Initialized."
    )