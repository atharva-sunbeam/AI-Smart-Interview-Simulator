"""
Resume Parser

Purpose:
Extract text from resume PDFs,
clean the text, and extract skills.
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
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "spark",
    "kafka",
    "airflow",
    "hadoop",
    "tableau",
    "power bi",
    "excel",
    "pandas",
    "numpy",
    "django",
    "flask",
    "fastapi",
    "docker",
    "postgresql",
    "mysql",
]


class ResumeParser:
    """
    Resume Parser class.
    """

    def extract_text_from_pdf(
        self,
        pdf_path,
    ):
        """
        Extract text from PDF resume.
        """

        text = ""

        pdf_path = Path(pdf_path)

        with open(
            pdf_path,
            "rb",
        ) as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    def clean_resume_text(
        self,
        text,
    ):
        """
        Clean extracted resume text.
        """

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        text = re.sub(
            r"[^a-zA-Z0-9+#.\s]",
            " ",
            text,
        )

        return text.strip()

    def extract_skills(
        self,
        text,
    ):
        """
        Extract skills using keyword matching.
        """

        extracted_skills = []

        for skill in SKILLS:

            pattern = (
                rf"\b{re.escape(skill.lower())}\b"
            )

            if re.search(
                pattern,
                text.lower(),
            ):
                extracted_skills.append(
                    skill
                )

        return sorted(
            list(
                set(extracted_skills)
            )
        )

    def parse_resume(
        self,
        pdf_path,
    ):
        """
        Complete resume parsing pipeline.

        Returns:

        {
            "raw_text": ...,
            "cleaned_text": ...,
            "skills": [...]
        }
        """

        text = self.extract_text_from_pdf(
            pdf_path
        )

        cleaned_text = (
            self.clean_resume_text(
                text
            )
        )

        skills = self.extract_skills(
            cleaned_text
        )

        return {
            "raw_text": text,
            "cleaned_text":
                cleaned_text,
            "skills": skills,
        }


if __name__ == "__main__":

    parser = ResumeParser()

    sample_resume = (
        "Resume.pdf"
    )

    try:

        result = (
            parser.parse_resume(
                sample_resume
            )
        )

        print(
            "\nExtracted Skills:"
        )

        print(
            result["skills"]
        )

    except Exception as error:

        print(
            f"Error: {error}"
        )