"""
Tests for Interview Session.
"""

from backend.interview_session import (
    InterviewSession,
)


def test_session_creation():

    session = InterviewSession()

    assert session is not None


def test_start_session():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    assert (
        session.current_role
        == "Python Developer"
    )


def test_submit_answer():

    session = InterviewSession()

    answer = (
        "Python decorators extend "
        "function behavior."
    )

    session.submit_answer(
        answer
    )

    assert (
        session.current_answer
        == answer
    )


def test_evaluate_answer():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    # Mock interview state
    session.current_question = (
        "What is Python?"
    )

    session.expected_answer = (
        "Python is a programming language."
    )

    session.submit_answer(
        "Python is a programming language."
    )

    result = (
        session.evaluate_answer()
    )

    assert "score" in result
    assert "feedback" in result
    assert "similarity" in result


def test_generate_report():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    # Mock interview state
    session.current_question = (
        "What is Python?"
    )

    session.expected_answer = (
        "Python is a programming language."
    )

    session.submit_answer(
        "Python is a programming language."
    )

    session.evaluate_answer()

    report = (
        session.generate_report()
    )

    assert (
        report["total_questions"]
        == 1
    )

    assert (
        report["average_score"]
        >= 0
    )

    assert (
        "overall_result"
        in report
    )

    assert (
        len(report["details"])
        == 1
    )