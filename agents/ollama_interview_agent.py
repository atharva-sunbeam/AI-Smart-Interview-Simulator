"""
Ollama Interview Agent

Purpose:
Generate intelligent interview questions,
follow-up questions, evaluate answer depth,
and summarize interview progress using
Ollama + Mistral.

Architecture:

InterviewSession
        ↓
QuestionGenerationAgent
        ↓
OllamaInterviewAgent
        ↓
Ollama
        ↓
Mistral 7B
"""

import sys
from pathlib import Path

import ollama

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from config.interview_prompts import (
    DEFAULT_MODEL,
    SYSTEM_PROMPT,
    QUESTION_PROMPT,
    FOLLOWUP_PROMPT,
    DEPTH_EVALUATION_PROMPT,
    SUMMARY_PROMPT,
)


class OllamaInterviewAgent:
    """
    AI Interview Brain powered by Ollama.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
    ):

        self.model = model

    def _generate(
        self,
        prompt: str,
    ) -> str:
        """
        Internal helper for generating responses.
        """

        try:

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            return (
                response["message"]["content"]
                .strip()
            )

        except Exception as error:

            return (
                f"Error communicating with Ollama: "
                f"{error}"
            )

    def generate_question(
        self,
        role: str,
        topic: str,
    ) -> str:
        """
        Generate an initial interview question.
        """

        prompt = QUESTION_PROMPT.format(
            role=role,
            topic=topic,
        )

        return self._generate(
            prompt
        )

    def generate_followup(
        self,
        role: str,
        topic: str,
        previous_question: str,
        candidate_answer: str,
    ) -> str:
        """
        Generate a follow-up question.
        """

        prompt = FOLLOWUP_PROMPT.format(
            role=role,
            topic=topic,
            question=previous_question,
            answer=candidate_answer,
        )

        return self._generate(
            prompt
        )

    def evaluate_depth(
        self,
        question: str,
        answer: str,
    ) -> str:
        """
        Evaluate depth of understanding.
        """

        prompt = DEPTH_EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
        )

        return self._generate(
            prompt
        )

    def summarize_interview_state(
        self,
        history: str,
    ) -> str:
        """
        Generate interview summary.
        """

        prompt = SUMMARY_PROMPT.format(
            history=history,
        )

        return self._generate(
            prompt
        )


def main():

    agent = OllamaInterviewAgent()

    print("=" * 60)
    print("OLLAMA INTERVIEW AGENT DEMO")
    print("=" * 60)

    question = agent.generate_question(
        role="Python Developer",
        topic="Decorators",
    )

    print("\nGenerated Question:\n")
    print(question)

    followup = agent.generate_followup(
        role="Python Developer",
        topic="Decorators",
        previous_question=question,
        candidate_answer=(
            "Decorators modify the behaviour "
            "of functions."
        ),
    )

    print("\nFollow-up Question:\n")
    print(followup)

    evaluation = agent.evaluate_depth(
        question=question,
        answer=(
            "Decorators modify the behaviour "
            "of functions."
        ),
    )

    print("\nDepth Evaluation:\n")
    print(evaluation)

    summary = agent.summarize_interview_state(
        history=f"""
Question:
{question}

Answer:
Decorators modify the behaviour of functions.
"""
    )

    print("\nInterview Summary:\n")
    print(summary)


if __name__ == "__main__":
    main()