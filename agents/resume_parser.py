"""
Resume Parser Agent

Purpose:
Extract text from resumes and identify
technical skills.

Pipeline:

PDF Resume
      ↓
Text Extraction
      ↓
Cleaning
      ↓
Skill Extraction
"""

import re
from pathlib import Path

import PyPDF2


SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "spark",
    "kafka",
    "airflow",
    "aws",
    "docker",
    "kubernetes",
    "etl",
    "power bi",
    "tableau",
    "excel",
]


class ResumeParser:
    """
    Resume Parser Agent
    """

    def extract_text_from_pdf(
        self,
        pdf_path
    ):
        """
        Extract text from PDF resume.
        """

        pdf_path = Path(pdf_path)

        text = ""

        with open(
            pdf_path,
            "rb"
        ) as file:

            reader = PyPDF2.PdfReader(
                file
            )

            for page in reader.pages:

                page_text = (
                    page.extract_text()
                )

                if page_text:
                    text += (
                        page_text + "\n"
                    )

        return text

    def clean_resume_text(
        self,
        text
    ):
        """
        Clean extracted resume text.
        """

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        text = re.sub(
            r"[^a-zA-Z0-9+#.\s]",
            " ",
            text
        )

        return text.strip()

    def extract_skills(
        self,
        text
    ):
        """
        Extract technical skills using
        keyword matching.
        """

        extracted_skills = []

        for skill in SKILLS:

            if skill.lower() in text:

                extracted_skills.append(
                    skill
                )

        return sorted(
            list(
                set(
                    extracted_skills
                )
            )
        )


def main():

    sample_resume = (
        "sample_resume.pdf"
    )

    parser = ResumeParser()

    try:

        text = (
            parser.extract_text_from_pdf(
                sample_resume
            )
        )

        cleaned_text = (
            parser.clean_resume_text(
                text
            )
        )

        skills = (
            parser.extract_skills(
                cleaned_text
            )
        )

        print(
            "\nExtracted Skills:\n"
        )

        for skill in skills:

            print(
                f"- {skill}"
            )

    except FileNotFoundError:

        print(
            "Sample resume not found."
        )


if __name__ == "__main__":
    main()