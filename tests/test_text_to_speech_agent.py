from pathlib import Path

from agents.text_to_speech_agent import (
    TextToSpeechAgent,
)


def test_agent_creation():

    agent = (
        TextToSpeechAgent()
    )

    assert agent is not None


def test_validate_text():

    agent = (
        TextToSpeechAgent()
    )

    assert (
        agent.validate_text(
            "Hello"
        )
        is True
    )

    assert (
        agent.validate_text(
            ""
        )
        is False
    )


def test_audio_generation():

    agent = (
        TextToSpeechAgent()
    )

    output = (
        "generated_audio/"
        "test_audio.mp3"
    )

    path = (
        agent.generate_audio(
            "Hello World",
            output,
        )
    )

    assert Path(
        path
    ).exists()