"""
Unit Tests for Ollama Interview Agent

Purpose:
Validate the functionality of the
Ollama Interview Agent.

Tests:
- Agent creation
- Question generation
- Follow-up generation
- Depth evaluation
- Interview summary
"""

from unittest.mock import patch
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.ollama_interview_agent import (
    OllamaInterviewAgent,
)


def mock_chat(*args, **kwargs):
    """
    Mock response from Ollama.
    """

    return {
        "message": {
            "content": "Mocked response from Ollama."
        }
    }


def test_agent_creation():
    """
    Test agent initialization.
    """

    agent = OllamaInterviewAgent()

    assert agent is not None


@patch(
    "agents.ollama_interview_agent.ollama.chat",
    side_effect=mock_chat,
)
def test_question_generation(mock_ollama):

    agent = OllamaInterviewAgent()

    response = agent.generate_question(
        role="Python Developer",
        topic="Decorators",
    )

    assert isinstance(response, str)
    assert response == "Mocked response from Ollama."


@patch(
    "agents.ollama_interview_agent.ollama.chat",
    side_effect=mock_chat,
)
def test_followup_generation(mock_ollama):

    agent = OllamaInterviewAgent()

    response = agent.generate_followup(
        role="Python Developer",
        topic="Decorators",
        previous_question="Explain decorators.",
        candidate_answer=(
            "Decorators modify functions."
        ),
    )

    assert isinstance(response, str)
    assert response == "Mocked response from Ollama."


@patch(
    "agents.ollama_interview_agent.ollama.chat",
    side_effect=mock_chat,
)
def test_depth_evaluation(mock_ollama):

    agent = OllamaInterviewAgent()

    response = agent.evaluate_depth(
        question="Explain decorators.",
        answer="Decorators modify functions.",
    )

    assert isinstance(response, str)
    assert response == "Mocked response from Ollama."


@patch(
    "agents.ollama_interview_agent.ollama.chat",
    side_effect=mock_chat,
)
def test_summary_generation(mock_ollama):

    agent = OllamaInterviewAgent()

    response = (
        agent.summarize_interview_state(
            history="""
Question:
Explain decorators.

Answer:
Decorators modify functions.
"""
        )
    )

    assert isinstance(response, str)
    assert response == "Mocked response from Ollama."