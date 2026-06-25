"""
System Controller

Purpose:
Coordinate the complete Smart Interview Simulator pipeline.

Pipeline:

Resume
    ↓
Resume Parser
    ↓
Role Prediction
    ↓
Question Generation
    ↓
Interview Session
    ↓
Answer Evaluation
    ↓
Report Generation
"""

from agents.resume_parser import ResumeParser
from agents.answer_evaluation_agent import AnswerEvaluationAgent
from backend.report_generator import ReportGenerator
from ml_models.role_prediction.train_role_classifier import RoleClassifier


class SystemController:
    """
    Orchestrates the complete interview workflow.
    """

    def __init__(self):
        self.resume_parser = ResumeParser()
        self.role_classifier = RoleClassifier()
        self.evaluator = AnswerEvaluationAgent()
        self.report_generator = ReportGenerator()

    def parse_resume(self, resume_path: str) -> str:
        """
        Extract and clean resume text.
        """

        print("Parsing resume...")

        resume_text = (
            self.resume_parser.extract_text_from_pdf(
                resume_path
            )
        )

        cleaned_text = (
            self.resume_parser.clean_resume_text(
                resume_text
            )
        )

        return cleaned_text

    def predict_role(self, resume_text: str) -> str:
        """
        Predict candidate role.
        """

        print("Predicting role...")

        try:
            self.role_classifier.load_model()

            predicted_role = (
                self.role_classifier.predict_role(
                    resume_text
                )
            )

            return predicted_role

        except FileNotFoundError:

            print(
                "Role prediction model not found. "
                "Using default role."
            )

            return "Python Developer"

        except Exception as error:

            print(
                f"Role Prediction Error: {error}"
            )

            return "Python Developer"

    def start_interview(
        self,
        role: str,
    ) -> list:
        """
        Start interview session.

        TODO:
        Replace placeholder questions with
        QuestionGenerationAgent.
        """

        print(
            f"Starting interview for: {role}"
        )

        questions = [
            "What is Python?",
            "Explain Object-Oriented Programming.",
            "What is inheritance?",
        ]

        return questions

    def evaluate_answers(
        self,
        expected_answers: list,
        candidate_answers: list,
    ) -> list:
        """
        Evaluate candidate answers.

        Returns complete evaluation
        results instead of only scores.
        """

        evaluation_results = []

        for expected, candidate in zip(
            expected_answers,
            candidate_answers,
        ):

            result = (
                self.evaluator.evaluate_answer(
                    expected_answer=expected,
                    candidate_answer=candidate,
                )
            )

            evaluation_results.append(result)

        return evaluation_results

    def generate_final_report(
        self,
        candidate_name: str,
        predicted_role: str,
        questions: list,
        evaluation_results: list,
    ) -> dict:
        """
        Generate final interview report.
        """

        scores = [
            result["score"]
            for result in evaluation_results
        ]

        average = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        strengths = []
        weaknesses = []
        recommendations = []

        for index, score in enumerate(scores):

            if score >= 80:

                strengths.append(
                    f"Question {index + 1}: "
                    "Strong answer."
                )

            elif score >= 60:

                weaknesses.append(
                    f"Question {index + 1}: "
                    "Needs more detail."
                )

                recommendations.append(
                    f"Revise concepts related to "
                    f"Question {index + 1}."
                )

            else:

                weaknesses.append(
                    f"Question {index + 1}: "
                    "Weak understanding."
                )

                recommendations.append(
                    f"Practice Question "
                    f"{index + 1} again."
                )

        report = (
            self.report_generator.generate_final_report(
                candidate_name=candidate_name,
                predicted_role=predicted_role,
                questions_asked=questions,
                scores=scores,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations,
            )
        )

        self.report_generator.save_report(
            report
        )

        return report

    def run_complete_pipeline(
        self,
        candidate_name: str,
        resume_path: str,
    ) -> dict:
        """
        Execute complete interview pipeline.
        """

        # -------------------------------
        # Step 1
        # Resume Parsing
        # -------------------------------

        resume_text = self.parse_resume(
            resume_path
        )

        # -------------------------------
        # Step 2
        # Role Prediction
        # -------------------------------

        predicted_role = self.predict_role(
            resume_text
        )

        # -------------------------------
        # Step 3
        # Interview Questions
        # -------------------------------

        questions = self.start_interview(
            predicted_role
        )

        # ------------------------------------
        # Placeholder
        #
        # Sprint 17:
        #
        # expected_answers
        #   ← Retrieved from RAG
        #
        # candidate_answers
        #   ← User answers from Streamlit
        # ------------------------------------

        expected_answers = questions

        candidate_answers = questions

        # -------------------------------
        # Step 4
        # Answer Evaluation
        # -------------------------------

        evaluation_results = (
            self.evaluate_answers(
                expected_answers,
                candidate_answers,
            )
        )

        # -------------------------------
        # Step 5
        # Report Generation
        # -------------------------------

        report = (
            self.generate_final_report(
                candidate_name=candidate_name,
                predicted_role=predicted_role,
                questions=questions,
                evaluation_results=evaluation_results,
            )
        )

        return report


if __name__ == "__main__":

    controller = SystemController()

    print(
        "System Controller initialized successfully."
    )

    # Example usage
    #
    # report = controller.run_complete_pipeline(
    #     candidate_name="John Doe",
    #     resume_path="resume.pdf",
    # )
    #
    # print(report)