"""
Tests for Question Generation Agent.
"""

from agents.question_generation_agent import (
    QuestionGenerationAgent,
)


def test_agent_creation():

    agent = QuestionGenerationAgent()

    assert agent is not None


def test_generate_question():

    agent = QuestionGenerationAgent()

    question = agent.generate_question(
        "Python Developer"
    )

    assert question is not None


def test_build_prompt():

    agent = QuestionGenerationAgent()

    prompt = agent.build_prompt(
        role="Python Developer",
        context=[
            "Python decorators modify function behavior."
        ]
    )

    assert "Candidate Role" in prompt
    assert "Relevant Context" in prompt