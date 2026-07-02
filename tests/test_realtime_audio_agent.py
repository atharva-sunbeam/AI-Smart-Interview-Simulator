"""
Unit Tests

Real-Time Audio Agent
"""

import numpy as np

from agents.realtime_audio_agent import (
    RealtimeAudioAgent,
)

from utils.voice_activity_detector import (
    VoiceActivityDetector,
)


# --------------------------------------------------
# Agent Creation
# --------------------------------------------------

def test_agent_creation():

    agent = (
        RealtimeAudioAgent()
    )

    assert agent is not None

    assert agent.streaming is False

    assert agent.get_live_transcript() == ""


# --------------------------------------------------
# Microphone Stream
# --------------------------------------------------

def test_microphone_stream():

    agent = (
        RealtimeAudioAgent()
    )

    #
    # Mock microphone start/stop
    #

    agent.audio_stream.start = (
        lambda: None
    )

    agent.audio_stream.stop = (
        lambda: None
    )

    agent.start_stream()

    assert (
        agent.is_streaming()
        is True
    )

    agent.stop_stream()

    assert (
        agent.is_streaming()
        is False
    )


# --------------------------------------------------
# Chunk Queue
# --------------------------------------------------

def test_chunk_creation():

    agent = (
        RealtimeAudioAgent()
    )

    sample_chunk = np.zeros(

        (32000, 1),

        dtype=np.float32,

    )

    agent.audio_stream.queue_chunk(
        sample_chunk
    )

    chunk = (
        agent.get_audio_chunk()
    )

    assert chunk is not None

    assert chunk.shape == (
        32000,
        1,
    )


# --------------------------------------------------
# Voice Activity Detection
# --------------------------------------------------

def test_vad():

    vad = (
        VoiceActivityDetector()
    )

    speech = np.ones(

        (32000, 1),

        dtype=np.float32,

    ) * 0.5

    silence = np.zeros(

        (32000, 1),

        dtype=np.float32,

    )

    assert (
        vad.is_speech(
            speech
        )
        is True
    )

    assert (
        vad.is_speech(
            silence
        )
        is False
    )


# --------------------------------------------------
# Transcript Handling
# --------------------------------------------------

def test_transcript_management():

    agent = (
        RealtimeAudioAgent()
    )

    agent.transcript = (
        "Hello"
    )

    assert (
        agent.get_live_transcript()
        == "Hello"
    )

    agent.clear_transcript()

    assert (
        agent.get_live_transcript()
        == ""
    )


# --------------------------------------------------
# Interviewer State
# --------------------------------------------------

def test_interviewer_state():

    agent = (
        RealtimeAudioAgent()
    )

    agent.set_interviewer_state(
        True
    )

    assert (
        agent.interviewer_speaking
        is True
    )

    agent.set_interviewer_state(
        False
    )

    assert (
        agent.interviewer_speaking
        is False
    )


# --------------------------------------------------
# Process Empty Stream
# --------------------------------------------------

def test_process_empty_stream():

    agent = (
        RealtimeAudioAgent()
    )

    result = (
        agent.process_next_chunk()
    )

    assert result is None