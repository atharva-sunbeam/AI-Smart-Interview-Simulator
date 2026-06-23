"""
Question Generation Agent

Purpose:
Generate interview questions based on
candidate role and RAG context.
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from rag_pipeline.retriever import Retriever


class QuestionGenerationAgent:
    """
    Agent responsible for generating
    interview questions.
    """

    def __init__(self):

        self.retriever = Retriever()

    def build_prompt(
        self,
        role,
        context
    ):
        """
        Build prompt for question generation.
        """

        formatted_context = (
            "\n----------------\n".join(
                context
            )
        )

        prompt = f"""
You are an expert technical interviewer.

Candidate Role:
{role}

Relevant Context:
{formatted_context}

Generate one technical interview question.
"""

        return prompt

    def generate_question(
        self,
        role
    ):
        """
        Generate interview question.
        """

        try:

            retrieved_chunks = (
                self.retriever.retrieve_context(
                    query=role,
                    top_k=3
                )
            )

            context = []

            for chunk in retrieved_chunks:

                if isinstance(chunk, dict):
                    context.append(
                        chunk.get(
                            "content",
                            ""
                        )
                    )
                else:
                    context.append(
                        str(chunk)
                    )

        except Exception:

            context = [
                "No context available."
            ]

        prompt = self.build_prompt(
            role=role,
            context=context
        )

        print("\nGenerated Prompt:\n")
        print(prompt)

        mock_questions = {
            "Python Developer":
                "Explain decorators in Python.",

            "Data Engineer":
                "Explain Kafka architecture and partitions.",

            "ML Engineer":
                "What is overfitting in Machine Learning?",

            "Data Analyst":
                "Explain the difference between INNER JOIN and LEFT JOIN."
        }

        return mock_questions.get(
            role,
            "Explain an important project you have worked on."
        )


def main():

    agent = QuestionGenerationAgent()

    role = "Python Developer"

    question = (
        agent.generate_question(
            role
        )
    )

    print("\nGenerated Question:\n")
    print(question)


if __name__ == "__main__":
    main()