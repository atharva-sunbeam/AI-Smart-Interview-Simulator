from backend.system_controller import (
    SystemController,
)


def test_controller_creation():

    controller = (
        SystemController()
    )

    assert controller is not None


def test_pipeline_method_exists():

    controller = (
        SystemController()
    )

    assert hasattr(
        controller,
        "run_complete_pipeline"
    )


def test_interview_methods_exist():

    controller = (
        SystemController()
    )

    assert hasattr(
        controller,
        "start_interview"
    )

    assert hasattr(
        controller,
        "ask_question"
    )

    assert hasattr(
        controller,
        "evaluate_answer"
    )