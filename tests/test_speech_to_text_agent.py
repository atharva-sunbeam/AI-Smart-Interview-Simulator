from pathlib import Path

import pytest

from agents.speech_to_text_agent import (
    SpeechToTextAgent
)


def test_agent_creation():

    agent = (
        SpeechToTextAgent()
    )

    assert agent is not None


def test_audio_validation():

    agent = (
        SpeechToTextAgent()
    )

    fake_audio = Path(
        "test.wav"
    )

    fake_audio.touch()

    assert (
        agent.validate_audio(
            fake_audio
        )
        is True
    )

    fake_audio.unlink()


def test_clean_transcript():

    agent = (
        SpeechToTextAgent()
    )

    text = (
        "   Python     is   great.   "
    )

    cleaned = (
        agent.clean_transcript(
            text
        )
    )

    assert (
        cleaned ==
        "Python is great."
    )


def test_invalid_audio():

    agent = (
        SpeechToTextAgent()
    )

    with pytest.raises(
        FileNotFoundError
    ):

        agent.validate_audio(
            "missing_audio.wav"
        )


def test_invalid_format():

    agent = (
        SpeechToTextAgent()
    )

    invalid_file = Path(
        "dummy.txt"
    )

    invalid_file.touch()

    with pytest.raises(
        ValueError
    ):

        agent.validate_audio(
            invalid_file
        )

    invalid_file.unlink()