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


def test_ask_question():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    question = (
        session.ask_question()
    )

    assert isinstance(
        question,
        str,
    )


def test_submit_answer():

    session = InterviewSession()

    session.submit_answer(
        "Sample answer"
    )

    assert (
        session.current_answer
        == "Sample answer"
    )


def test_evaluate_answer():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    session.current_question = (
        "Explain decorators."
    )

    session.expected_answer = (
        "Decorators modify the behavior "
        "of functions."
    )

    session.submit_answer(
        "Decorators modify functions."
    )

    result = (
        session.evaluate_answer()
    )

    assert "score" in result

    assert "feedback" in result


def test_generate_report():

    session = InterviewSession()

    session.start_session(
        "Python Developer"
    )

    session.current_question = (
        "Explain decorators."
    )

    session.expected_answer = (
        "Decorators modify the behavior "
        "of functions."
    )

    session.submit_answer(
        "Decorators modify functions."
    )

    session.evaluate_answer()

    report = (
        session.generate_report()
    )

    assert (
        report["total_questions"]
        == 1
    )