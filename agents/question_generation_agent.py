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

Generate one {role} interview question
with {role} difficulty level.
"""

    def generate_question(
        self,
        role,
        difficulty="Medium",
    ):
        """
        Generate role-specific question.

        Returns:

        {{
            "question": "...",
            "expected_answer": "...",
            "context": [...],
            "prompt": "...",
            "difficulty": "..."
        }}
        """

        try:

            retrieved_context = (
                self.retriever.retrieve_context(
                    query=role,
                    top_k=3,
                )
            )

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

        mock_questions = {

            "Python Developer": {

                "Easy": {
                    "question":
                        "What is Python?",

                    "expected_answer":
                        "Python is a high-level interpreted programming language."
                },

                "Medium": {
                    "question":
                        "Explain decorators in Python.",

                    "expected_answer":
                        "Decorators extend the behaviour of functions without modifying their source code."
                },

                "Hard": {
                    "question":
                        "Explain metaclasses in Python.",

                    "expected_answer":
                        "Metaclasses define how classes are created in Python."
                }
            },

            "Data Engineer": {

                "Easy": {
                    "question":
                        "What is Apache Kafka?",

                    "expected_answer":
                        "Kafka is a distributed event streaming platform."
                },

                "Medium": {
                    "question":
                        "Explain Kafka architecture.",

                    "expected_answer":
                        "Kafka consists of producers, brokers, topics, partitions and consumers."
                },

                "Hard": {
                    "question":
                        "Explain Kafka consumer rebalance protocol.",

                    "expected_answer":
                        "Kafka rebalancing redistributes partitions among consumers when group membership changes."
                }
            },

            "ML Engineer": {

                "Easy": {
                    "question":
                        "What is Machine Learning?",

                    "expected_answer":
                        "Machine Learning enables systems to learn patterns from data."
                },

                "Medium": {
                    "question":
                        "What is overfitting in Machine Learning?",

                    "expected_answer":
                        "Overfitting occurs when a model learns training data too closely and performs poorly on unseen data."
                },

                "Hard": {
                    "question":
                        "Explain bias-variance tradeoff.",

                    "expected_answer":
                        "Bias-variance tradeoff balances model simplicity and generalization."
                }
            },

            "Data Analyst": {

                "Easy": {
                    "question":
                        "What is SQL?",

                    "expected_answer":
                        "SQL is a language used to query relational databases."
                },

                "Medium": {
                    "question":
                        "What is the difference between INNER JOIN and LEFT JOIN?",

                    "expected_answer":
                        "INNER JOIN returns matching rows from both tables, whereas LEFT JOIN returns all rows from the left table and matching rows from the right table."
                },

                "Hard": {
                    "question":
                        "Explain window functions in SQL.",

                    "expected_answer":
                        "Window functions perform calculations across related rows without collapsing them."
                }
            }
        }

        role_questions = mock_questions.get(
            role
        )

        if role_questions:

            result = role_questions.get(
                difficulty,
                role_questions["Medium"]
            )

        else:

            result = {

                "question":
                    "Explain an important project.",

                "expected_answer":
                    "Candidate should explain project."
            }

        result["context"] = (
            formatted_context
        )

        result["prompt"] = (
            prompt
        )

        result["difficulty"] = (
            difficulty
        )

        return result


def main():

    agent = (
        QuestionGenerationAgent()
    )

    result = (
        agent.generate_question(
            role="Python Developer",
            difficulty="Medium"
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