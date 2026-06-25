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

    def parse_resume(self, resume_path):
        """
        Parse candidate resume.
        """
        print("Parsing resume...")
        return self.resume_parser.parse_resume(resume_path)

    def predict_role(self, resume_text):
        """
        Predict candidate role.
        """
        print("Predicting role...")

        try:
            self.role_classifier.load_model()
            return self.role_classifier.predict_role(resume_text)
        except Exception:
            return "Python Developer"

    def start_interview(self, role):
        """
        Start interview session.

        Placeholder until Question Generation
        Agent is fully integrated.
        """
        print(f"Starting {role} interview...")

        return [
            "What is Python?",
            "Explain Object-Oriented Programming.",
            "What is inheritance?",
        ]

    def evaluate_answers(
        self,
        expected_answers,
        candidate_answers,
    ):
        """
        Evaluate candidate answers.
        """

        scores = []

        for expected, candidate in zip(
            expected_answers,
            candidate_answers,
        ):
            result = self.evaluator.evaluate_answer(
                expected_answer=expected,
                candidate_answer=candidate,
            )

            scores.append(result["score"])

        return scores

    def generate_final_report(
        self,
        candidate_name,
        predicted_role,
        questions,
        scores,
    ):
        """
        Generate interview report.
        """

        strengths = []
        weaknesses = []
        recommendations = []

        average = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        if average >= 80:
            strengths.append(
                "Strong technical understanding."
            )

        elif average >= 60:
            strengths.append(
                "Good foundational knowledge."
            )
            weaknesses.append(
                "Some concepts need improvement."
            )
            recommendations.append(
                "Practice more interview questions."
            )

        else:
            weaknesses.append(
                "Core technical concepts need improvement."
            )
            recommendations.extend(
                [
                    "Review programming fundamentals.",
                    "Practice technical interviews.",
                ]
            )

        report = self.report_generator.generate_final_report(
            candidate_name=candidate_name,
            predicted_role=predicted_role,
            questions_asked=questions,
            scores=scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )

        self.report_generator.save_report(report)

        return report

    def run_complete_pipeline(
        self,
        candidate_name,
        resume_path,
    ):
        """
        Execute the complete interview workflow.
        """

        resume_text = self.parse_resume(resume_path)

        predicted_role = self.predict_role(
            resume_text
        )

        questions = self.start_interview(
            predicted_role
        )

        # Placeholder expected answers
        expected_answers = questions

        # Placeholder candidate answers
        candidate_answers = questions

        scores = self.evaluate_answers(
            expected_answers,
            candidate_answers,
        )

        report = self.generate_final_report(
            candidate_name=candidate_name,
            predicted_role=predicted_role,
            questions=questions,
            scores=scores,
        )

        return report

if __name__ == "__main__":


    controller = SystemController()

    print(
        "System Controller initialized."
    )
    
