
from backend.interview_session import (
    InterviewSession,
)


def test_evaluate_answer():

    session = InterviewSession()

    result = session.evaluate_answer(
        expected_answer="Python is a programming language.",
        candidate_answer="Python is a programming language.",
    )

    assert "score" in result
    assert "feedback" in result
    assert "similarity" in result


def test_submit_answer():

    session = InterviewSession()

    result = session.submit_answer(
        question="What is Python?",
        expected_answer="Python is a programming language.",
        candidate_answer="Python is a programming language.",
    )

    assert result["score"] >= 90
