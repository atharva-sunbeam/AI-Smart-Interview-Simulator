from backend.interview_session import (
    InterviewSession
)


def test_session_creation():

    session = InterviewSession()

    assert session is not None


def test_stt_agent_present():

    session = InterviewSession()

    assert (
        session.stt_agent
        is not None
    )