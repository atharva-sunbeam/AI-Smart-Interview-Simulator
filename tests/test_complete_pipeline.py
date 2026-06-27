"""
End-to-End System Test

Pipeline:

Resume
    ↓
Parse Resume
    ↓
Predict Role
    ↓
Generate Question
    ↓
Submit Answer
    ↓
Evaluate Answer
    ↓
Generate Report
"""

from backend.system_controller import (
    SystemController,
)


def test_controller_creation():

    controller = SystemController()

    assert controller is not None


def test_complete_pipeline():

    controller = SystemController()

    controller.start_interview(
        "Python Developer"
    )

    question = (
        controller.ask_question()
    )

    assert question is not None

    controller.submit_answer(
        "Decorators modify the behavior "
        "of functions."
    )

    evaluation = (
        controller.evaluate_answer()
    )

    assert evaluation is not None

    assert "score" in evaluation

    report = (
        controller.generate_report()
    )

    assert report is not None

    assert "average_score" in report


def test_question_generation():

    controller = SystemController()

    controller.start_interview(
        "Python Developer"
    )

    question = (
        controller.ask_question()
    )

    assert isinstance(
        question,
        str,
    )


def test_report_generation():

    controller = SystemController()

    controller.start_interview(
        "Python Developer"
    )

    controller.ask_question()

    controller.submit_answer(
        "Decorators are wrappers."
    )

    controller.evaluate_answer()

    report = (
        controller.generate_report()
    )

    assert (
        report["total_questions"]
        >= 1
    )