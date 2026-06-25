"""
Question Generation Agent
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from rag_pipeline.retriever import (
    Retriever,
)


class QuestionGenerationAgent:

    def __init__(self):

        self.retriever = Retriever()

    def build_prompt(
        self,
        role,
        context
    ):

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

Generate ONE interview question from the context.
"""

    def generate_question(
        self,
        role
    ):

        try:

            retrieved_context = (
                self.retriever.retrieve_context(
                    query=role,
                    top_k=3
                )
            )

            formatted_context = (
                self.retriever.format_context(
                    retrieved_context
                )
            )

        except Exception:

            formatted_context = [
                "What are decorators in Python?"
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
        # Temporary mock LLM output.
        # Future:
        # Ollama/Mistral
        #

        question = (
            "Explain decorators in Python."
        )

        expected_answer = (
            "Decorators are functions "
            "that modify or extend "
            "the behavior of other "
            "functions without changing "
            "their source code."
        )

        return {
            "question": question,
            "expected_answer": expected_answer,
            "context": formatted_context,
            "prompt": prompt,
        }


if __name__ == "__main__":

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