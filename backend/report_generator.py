"""
Report Generator

Purpose:
Generate and save the final interview report.
"""

import json
from pathlib import Path

class ReportGenerator:
    """
    Generates the final interview report.
    """

    
    def generate_final_report(
        self,
        candidate_name,
        predicted_role,
        questions_asked,
        scores,
        strengths,
        weaknesses,
        recommendations,
    ):
        """
        Generate interview report as a dictionary.
        """

        average_score = (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0
        )

        report = {
            "candidate_name": candidate_name,
            "predicted_role": predicted_role,
            "questions_asked": questions_asked,
            "scores": scores,
            "average_score": average_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }

        return report

    def save_report(
        self,
        report,
        output_file="reports/interview_report.json",
    ):
        """
        Save report as JSON.
        """

        output_path = Path(output_file)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
            )

        print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    
    generator = ReportGenerator()

    report = generator.generate_final_report(
        candidate_name="John Doe",
        predicted_role="Data Engineer",
        questions_asked=[
            "What is Python?",
            "Explain Kafka.",
            "What is ETL?",
        ],
        scores=[82, 76, 88],
        strengths=[
            "Strong Python knowledge",
            "Good SQL understanding",
        ],
        weaknesses=[
            "Limited Kafka concepts",
        ],
        recommendations=[
            "Study Kafka architecture",
            "Practice Spark interview questions",
        ],
    )

    generator.save_report(report)

    print(report)

