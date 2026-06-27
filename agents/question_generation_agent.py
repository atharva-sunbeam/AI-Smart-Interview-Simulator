"""
Question Generation Agent

Purpose:
Generate role-specific interview questions.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from rag_pipeline.retriever import Retriever


class QuestionGenerationAgent:
    """
    Generates interview questions.
    """

    def __init__(self):

        self.retriever = Retriever()

    def build_prompt(
        self,
        role,
        context,
    ):
        """
        Build prompt for future LLM integration.
        """

        context_text = (
            "\n----------------\n".join(
                context
            )
        )

        return f"""
You are an expert technical interviewer.

Candidate Role:
{role}

Relevant Context:
{context_text}

Generate one technical interview question.
"""

    def generate_question(
        self,
        role,
    ):
        """
        Generate role-specific question.

        Returns:

        {
            "question": "...",
            "expected_answer": "...",
            "context": [...],
            "prompt": "..."
        }
        """

        try:

            retrieved_context = (
                self.retriever.retrieve_context(
                    query=role,
                    top_k=3,
                )
            )

            #
            # Convert retrieved chunks into
            # a list of text chunks.
            #

            formatted_context = []

            for chunk in retrieved_context:

                if isinstance(
                    chunk,
                    dict
                ):

                    formatted_context.append(
                        chunk.get(
                            "content",
                            ""
                        )
                    )

                else:

                    formatted_context.append(
                        str(chunk)
                    )

        except Exception:

            formatted_context = [
                "No context available."
            ]

        prompt = self.build_prompt(
            role=role,
            context=formatted_context,
        )

        print(
            "\nGenerated Prompt:\n"
        )

        print(prompt)

        #
        # Temporary mock questions.
        # Replace with Ollama/Mistral later.
        #

        mock_questions = {

            "Python Developer": {

                "question":
                    "Explain decorators in Python.",

                "expected_answer":
                    "Decorators extend the behaviour "
                    "of functions without modifying "
                    "their source code."
            },

            "Data Engineer": {

                "question":
                    "Explain Kafka architecture.",

                "expected_answer":
                    "Kafka is a distributed streaming "
                    "platform consisting of producers, "
                    "brokers and consumers."
            },

            "ML Engineer": {

                "question":
                    "What is overfitting in Machine Learning?",

                "expected_answer":
                    "Overfitting occurs when a model "
                    "learns training data too closely "
                    "and performs poorly on unseen data."
            },

            "Data Analyst": {

                "question":
                    "What is the difference between "
                    "INNER JOIN and LEFT JOIN?",

                "expected_answer":
                    "INNER JOIN returns matching rows "
                    "from both tables, whereas LEFT JOIN "
                    "returns all rows from the left table "
                    "and matching rows from the right table."
            }
        }

        result = mock_questions.get(

            role,

            {
                "question":
                    "Explain an important project.",

                "expected_answer":
                    "Candidate should explain project."
            }
        )

        result["context"] = (
            formatted_context
        )

        result["prompt"] = (
            prompt
        )

        return result


def main():

    agent = (
        QuestionGenerationAgent()
    )

    result = (
        agent.generate_question(
            "Python Developer"
        )
    )

    print(
        "\nGenerated Question:\n"
    )

    print(
        result["question"]
    )

    print(
        "\nExpected Answer:\n"
    )

    print(
        result["expected_answer"]
    )


if __name__ == "__main__":
    main()