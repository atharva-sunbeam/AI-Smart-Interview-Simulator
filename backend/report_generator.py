"""
Report Generator

Purpose:
Generate and save the final interview report.
"""

import json
from pathlib import Path
from datetime import datetime


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

        if average_score >= 80:
            overall_result = "Excellent"

        elif average_score >= 60:
            overall_result = "Good"

        else:
            overall_result = "Needs Improvement"

        report = {
            "candidate_name": candidate_name,
            "predicted_role": predicted_role,
            "interview_date": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "questions_asked": questions_asked,
            "scores": scores,
            "average_score": average_score,
            "overall_result": overall_result,
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

    print("\nInterview Report")
    print("-" * 40)

    for key, value in report.items():
        print(f"{key}: {value}")